"""ReportLab PDF: testimony, timelines, pitch formula, BNS list, content SHA-256."""
import hashlib
import io
import json
from datetime import datetime, timezone

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def _esc(s: str) -> str:
    return (
        (s or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _story(
    case_id: str,
    counselor_name: str,
    structured_testimony: str,
    timeline_events: list,
    knowledge_graph_summary: str,
    verified_bns: list[dict],
    content_hash: str,
    pitch_reconstructed: list | None,
    pitch_formula: str,
) -> list:
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("<b>Nyaya legal aid draft</b>", styles["Title"]))
    story.append(Paragraph(f"Case: {case_id} &nbsp; Counselor: {counselor_name}", styles["Normal"]))
    story.append(Paragraph(
        f"Generated (UTC): {datetime.now(timezone.utc).isoformat()}",
        styles["Normal"],
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Structured testimony (AI-assisted draft)</b>", styles["Heading2"]))
    for block in structured_testimony.split("\n\n"):
        if block.strip():
            story.append(Paragraph(_esc(block).replace("\n", "<br/>")[:4000], styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Possibility-weighted reconstruction</b>", styles["Heading2"]))
    story.append(Paragraph(_esc(pitch_formula or "P = 0.54·voice + 0.32·words + 0.14·facial"), styles["Normal"]))
    story.append(Paragraph(
        "<i>Modality fusion for counselor structuring — not a claim of legal fact.</i>",
        styles["Italic"],
    ))
    story.append(Spacer(1, 6))
    for row in pitch_reconstructed or []:
        line = f"#{row.get('rank')} {row.get('event_id', '')} P={row.get('possibility')} [{row.get('confidence_band', '')}]: {row.get('summary', '')[:400]}"
        story.append(Paragraph(_esc(line), styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>AI-reconstructed timeline (Bayesian cues)</b>", styles["Heading2"]))
    story.append(Paragraph(
        "<i>Approximate order only — may be incomplete — not a statement of fact — subject to legal review.</i>",
        styles["Italic"],
    ))
    story.append(Spacer(1, 6))
    for ev in timeline_events or []:
        cid = ev.get("event_id", "")
        txt = (ev.get("event_text") or "")[:500]
        cert = ev.get("bayesian_certainty", "")
        story.append(Paragraph(_esc(f"{cid} (certainty {cert}): {txt}"), styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Entity / relationship summary</b>", styles["Heading2"]))
    story.append(Paragraph(_esc(knowledge_graph_summary).replace("\n", "<br/>")[:3000], styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Verified BNS sections (counselor confirmed)</b>", styles["Heading2"]))
    for b in verified_bns:
        story.append(Paragraph(f"• {b.get('id', '')} — {b.get('title', '')}", styles["BodyText"]))
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        f"<b>Content fingerprint (SHA-256 of canonical payload)</b><br/>{content_hash}",
        styles["Normal"],
    ))
    return story


def compute_content_fingerprint(
    case_id: str,
    counselor_name: str,
    structured_testimony: str,
    timeline_events: list,
    knowledge_graph_summary: str,
    verified_bns: list[dict],
    pitch_reconstructed: list | None = None,
) -> str:
    payload = json.dumps(
        {
            "case_id": case_id,
            "counselor_name": counselor_name,
            "structured_testimony": structured_testimony,
            "timeline_events": timeline_events,
            "knowledge_graph_summary": knowledge_graph_summary,
            "verified_bns": verified_bns,
            "pitch_reconstructed": pitch_reconstructed or [],
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_pdf_bytes(
    case_id: str,
    counselor_name: str,
    structured_testimony: str,
    timeline_events: list,
    knowledge_graph_summary: str,
    verified_bns: list[dict],
    pitch_reconstructed: list | None = None,
    pitch_formula: str = "",
) -> tuple[bytes, str]:
    content_hash = compute_content_fingerprint(
        case_id,
        counselor_name,
        structured_testimony,
        timeline_events,
        knowledge_graph_summary,
        verified_bns,
        pitch_reconstructed,
    )
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, title=f"Nyaya — {case_id}")
    doc.build(
        _story(
            case_id,
            counselor_name,
            structured_testimony,
            timeline_events,
            knowledge_graph_summary,
            verified_bns,
            content_hash,
            pitch_reconstructed,
            pitch_formula,
        )
    )
    return buf.getvalue(), content_hash
