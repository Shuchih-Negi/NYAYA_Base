import base64
import json
import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy import func
from sqlalchemy.orm import Session

load_dotenv()

from app.database import get_db, init_db
from app.models import Case, Transcript
from app.schemas import (
    BrainMappingRequest,
    CaseCreate,
    GuidanceRequest,
    SyntheticBrainRequest,
    TranscriptChunkIn,
    VerifyBnsRequest,
)

from services.brain_mapping_plotter import plot_brain_mapping_figure
from services.bayesian_timeline import reconstruct_timeline
from services.bns_faiss import search_bns
from services.gemini_service import (
    counselor_guidance,
    extract_knowledge_graph,
    structured_testimony_for_pdf,
)
from services.pdf_export import build_pdf_bytes
from services.pitch_timeline import build_pitch_timeline
from services.semantic_edges import compute_semantic_edges
from services.tribe_synthetic import (
    project_modalities_from_text,
    synthesize_wave_from_text,
    synthetic_trauma_description,
    tribe_notes,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Nyaya API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/brain-mapping", tags=["Analysis"])
def brain_mapping(body: BrainMappingRequest):
    """
    Matplotlib figure: 4 brain heatmaps + 15-segment stimulus bar (fire cmap, p99 norm).
    Random fields seeded from voice/words/face/P and optional stress trace.
    """
    png, meta = plot_brain_mapping_figure(
        body.voice,
        body.words,
        body.face,
        body.possibility,
        body.stress_points or None,
        n_timesteps=body.n_timesteps,
        norm_percentile=99,
        vmin=0.6,
        alpha_cmap=(0.0, 0.2),
        show_stimuli=True,
    )
    return {
        "image_b64": base64.b64encode(png).decode("ascii"),
        "meta": meta,
    }


@app.post("/api/brain-mapping/synthetic", tags=["Analysis"])
def synthetic_brain_mapping(body: SyntheticBrainRequest):
    """
    Build a realistic synthetic testimony paragraph, convert it to a simple
    playable waveform, derive proxy modality scores, and return a 2x2 brain map.
    """
    description = synthetic_trauma_description(body.spoken_sample or "")
    projection = project_modalities_from_text(description)
    wav = synthesize_wave_from_text(description)
    png, meta = plot_brain_mapping_figure(
        projection.voice,
        projection.words,
        projection.face,
        projection.possibility,
        projection.stress_points,
        n_timesteps=body.n_timesteps,
        norm_percentile=99,
        vmin=0.6,
        alpha_cmap=(0.0, 0.2),
        show_stimuli=True,
    )

    variants = [
        (projection.voice, projection.words, projection.face, projection.possibility),
        (min(1.0, projection.voice + 0.08), projection.words, projection.face, min(1.0, projection.possibility + 0.04)),
        (projection.voice, min(1.0, projection.words + 0.08), projection.face, min(1.0, projection.possibility + 0.04)),
        (projection.voice, projection.words, min(1.0, projection.face + 0.08), min(1.0, projection.possibility + 0.04)),
    ]
    grid = []
    for v, w, f, p in variants:
        panel_png, _ = plot_brain_mapping_figure(
            v,
            w,
            f,
            p,
            projection.stress_points,
            n_timesteps=body.n_timesteps,
            norm_percentile=99,
            vmin=0.6,
            alpha_cmap=(0.0, 0.2),
            show_stimuli=False,
        )
        grid.append(base64.b64encode(panel_png).decode("ascii"))

    return {
        "description": description,
        "audio_wav_b64": base64.b64encode(wav).decode("ascii"),
        "brain_image_b64": base64.b64encode(png).decode("ascii"),
        "brain_grid_b64": grid,
        "modalities": {
            "voice": projection.voice,
            "words": projection.words,
            "face": projection.face,
            "possibility": projection.possibility,
            "stress_points": projection.stress_points,
            "method": projection.method,
        },
        "meta": {
            **meta,
            "layout": "2x2",
            "tribe_mode": projection.method,
            "tribe_usage_notes": tribe_notes(),
        },
    }


@app.post("/api/cases", tags=["Cases"])
def create_case(body: CaseCreate, db: Session = Depends(get_db)):
    existing = db.query(Case).filter(Case.case_id == body.case_id).first()
    if existing:
        return {"case_id": existing.case_id, "counselor_name": existing.counselor_name}
    c = Case(case_id=body.case_id, counselor_name=body.counselor_name)
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"case_id": c.case_id, "counselor_name": c.counselor_name}


@app.get("/api/cases/{case_id}", tags=["Cases"])
def get_case(case_id: str, db: Session = Depends(get_db)):
    c = db.query(Case).filter(Case.case_id == case_id).first()
    if not c:
        raise HTTPException(404, "Case not found")
    rows = (
        db.query(Transcript)
        .filter(Transcript.case_id == case_id)
        .order_by(Transcript.chunk_index)
        .all()
    )
    return {
        "case_id": c.case_id,
        "counselor_name": c.counselor_name,
        "pdf_hash": c.pdf_hash,
        "verified_bns": json.loads(c.verified_bns or "[]"),
        "transcripts": [
            {
                "chunk_index": t.chunk_index,
                "text": t.text,
                "stress_label": t.stress_label,
                "stress_score": t.stress_score,
                "signal_voice": t.signal_voice,
                "signal_words": t.signal_words,
                "signal_face": t.signal_face,
                "possibility": t.possibility,
            }
            for t in rows
        ],
    }


@app.post("/api/cases/{case_id}/transcripts", tags=["Cases"])
def append_transcript(case_id: str, body: TranscriptChunkIn, db: Session = Depends(get_db)):
    c = db.query(Case).filter(Case.case_id == case_id).first()
    if not c:
        raise HTTPException(404, "Case not found")
    max_idx = db.query(func.max(Transcript.chunk_index)).filter(Transcript.case_id == case_id).scalar()
    next_idx = (max_idx + 1) if max_idx is not None else 0
    idx = body.chunk_index if body.chunk_index is not None else next_idx
    t = Transcript(
        case_id=case_id,
        chunk_index=idx,
        text=body.text,
        stress_label=body.stress_label,
        stress_score=body.stress_score,
        signal_voice=body.signal_voice,
        signal_words=body.signal_words,
        signal_face=body.signal_face,
        possibility=body.possibility,
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return {"ok": True, "id": t.id, "chunk_index": t.chunk_index}


@app.post("/api/demo/load", tags=["Demo"])
def load_demo(db: Session = Depends(get_db)):
    path = Path(__file__).resolve().parent.parent / "data" / "demo_testimony.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    cid = data["case_id"]
    c = db.query(Case).filter(Case.case_id == cid).first()
    if not c:
        c = Case(case_id=cid, counselor_name=data.get("counselor_name", "Sunita Sharma"))
        db.add(c)
    else:
        c.counselor_name = data.get("counselor_name", c.counselor_name)
    db.query(Transcript).filter(Transcript.case_id == cid).delete()
    for ch in data["chunks"]:
        db.add(
            Transcript(
                case_id=cid,
                chunk_index=ch["chunk_index"],
                text=ch["text"],
                stress_label=ch.get("stress_label"),
                stress_score=ch.get("stress_score"),
                signal_voice=ch.get("signal_voice"),
                signal_words=ch.get("signal_words"),
                signal_face=ch.get("signal_face"),
                possibility=ch.get("possibility"),
            )
        )
    db.commit()
    return {"ok": True, "case_id": cid}


@app.post("/api/pitch-timeline", tags=["Analysis"])
def pitch_timeline(case_id: str = Query(...), db: Session = Depends(get_db)):
    rows = (
        db.query(Transcript)
        .filter(Transcript.case_id == case_id)
        .order_by(Transcript.chunk_index)
        .all()
    )
    return build_pitch_timeline(rows)


@app.post("/api/bayesian-timeline", tags=["Analysis"])
def bayesian_timeline(case_id: str = Query(...), db: Session = Depends(get_db)):
    rows = (
        db.query(Transcript)
        .filter(Transcript.case_id == case_id)
        .order_by(Transcript.chunk_index)
        .all()
    )
    text = " ".join(t.text for t in rows)
    if not text.strip():
        return []
    return reconstruct_timeline(text)


@app.post("/api/semantic-edges", tags=["Analysis"])
def semantic_edges(case_id: str = Query(...), db: Session = Depends(get_db)):
    rows = (
        db.query(Transcript)
        .filter(Transcript.case_id == case_id)
        .order_by(Transcript.chunk_index)
        .all()
    )
    return compute_semantic_edges(rows)


@app.post("/api/gemini/guidance", tags=["Gemini"])
def api_guidance(body: GuidanceRequest):
    return {"guidance": counselor_guidance(body.transcript_window)}


@app.post("/api/gemini/knowledge-graph", tags=["Gemini"])
def api_knowledge_graph(case_id: str = Query(...), db: Session = Depends(get_db)):
    rows = (
        db.query(Transcript)
        .filter(Transcript.case_id == case_id)
        .order_by(Transcript.chunk_index)
        .all()
    )
    text = " ".join(t.text for t in rows)
    return extract_knowledge_graph(text)


@app.get("/api/bns/suggest", tags=["BNS"])
def bns_suggest(case_id: str = Query(...), db: Session = Depends(get_db)):
    rows = (
        db.query(Transcript)
        .filter(Transcript.case_id == case_id)
        .order_by(Transcript.chunk_index)
        .all()
    )
    text = " ".join(t.text for t in rows)
    return {"suggestions": search_bns(text, top_k=5)}


@app.post("/api/cases/{case_id}/verify-bns", tags=["Cases"])
def verify_bns(case_id: str, body: VerifyBnsRequest, db: Session = Depends(get_db)):
    c = db.query(Case).filter(Case.case_id == case_id).first()
    if not c:
        raise HTTPException(404, "Case not found")
    c.verified_bns = json.dumps(body.section_ids)
    db.commit()
    return {"ok": True, "verified_bns": body.section_ids}


@app.post("/api/cases/{case_id}/pdf", tags=["Cases"])
def generate_pdf(case_id: str, db: Session = Depends(get_db)):
    c = db.query(Case).filter(Case.case_id == case_id).first()
    if not c:
        raise HTTPException(404, "Case not found")
    verified_ids = json.loads(c.verified_bns or "[]")
    if not verified_ids:
        raise HTTPException(400, "Select at least one BNS section before generating PDF")

    rows = (
        db.query(Transcript)
        .filter(Transcript.case_id == case_id)
        .order_by(Transcript.chunk_index)
        .all()
    )
    full_text = " ".join(t.text for t in rows)
    timeline = reconstruct_timeline(full_text)
    pitch = build_pitch_timeline(rows)
    structured = structured_testimony_for_pdf(full_text, timeline)
    kg = extract_knowledge_graph(full_text)
    kg_summary = json.dumps(kg, ensure_ascii=False, indent=2)[:4000]

    path = Path(__file__).resolve().parent.parent / "data" / "bns_sections.json"
    with open(path, encoding="utf-8") as f:
        all_sections = {s["id"]: s for s in json.load(f)}
    verified_bns = [all_sections[i] for i in verified_ids if i in all_sections]

    pdf_bytes, digest = build_pdf_bytes(
        case_id,
        c.counselor_name,
        structured,
        timeline,
        kg_summary,
        verified_bns,
        pitch_reconstructed=pitch.get("reconstructed_timeline"),
        pitch_formula=pitch.get("formula", ""),
    )
    c.pdf_hash = digest
    db.commit()
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="nyaya-{case_id}.pdf"',
            "X-Content-Fingerprint": digest,
        },
    )
