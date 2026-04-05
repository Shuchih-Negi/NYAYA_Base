"""
Pitch timeline: possibility = 0.54*voice + 0.32*words + 0.14*facial
Events + sub-nodes + reconstructed ordering (demo/heuristic layer).
"""
import re

WEIGHT_VOICE = 0.54
WEIGHT_WORDS = 0.32
WEIGHT_FACE = 0.14

HEDGE = re.compile(
    r"\b(maybe|perhaps|i think|i guess|not sure|unsure|shayad|lagta|lag raha)\b",
    re.I,
)
ASSERT = re.compile(
    r"\b(always|never|definitely|sure|certain|forced|locked|threat|rape|hit|struck)\b",
    re.I,
)
TEMPORAL = re.compile(
    r"\b(then|after|before|next|january|february|march|april|may|june|july|august|september|october|november|december|monday|tuesday|phir|pehle|baad)\b",
    re.I,
)


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def possibility(voice: float, words: float, facial: float) -> float:
    return clamp01(
        WEIGHT_VOICE * clamp01(voice)
        + WEIGHT_WORDS * clamp01(words)
        + WEIGHT_FACE * clamp01(facial)
    )


def words_score_from_text(text: str) -> float:
    """Lightweight NLP proxy: assertive vs hedging density."""
    t = (text or "").strip()
    if not t:
        return 0.45
    h = len(HEDGE.findall(t))
    a = len(ASSERT.findall(t))
    tl = 1 if TEMPORAL.search(t) else 0
    # More assertions + temporal anchors => higher words channel
    raw = 0.42 + 0.08 * min(a, 4) - 0.06 * min(h, 4) + 0.05 * tl
    return clamp01(raw + 0.04 * min(len(t) / 200.0, 1.0))


def split_sub_nodes(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?।])\s+", (text or "").strip())
    return [p for p in parts if len(p) > 8][:6] or ([text[:120]] if text else [])


def build_pitch_timeline(rows: list) -> dict:
    """
    rows: ORM Transcript with text, signal_voice, signal_face, possibility, etc.
    """
    if not rows:
        return {
            "formula": f"P = {WEIGHT_VOICE}·V + {WEIGHT_WORDS}·W + {WEIGHT_FACE}·F",
            "events": [],
            "reconstructed_timeline": [],
        }

    events = []
    event_id = 0

    for r in rows:
        voice = clamp01(getattr(r, "signal_voice", None) or getattr(r, "stress_score", None) or 0.35)
        face = clamp01(getattr(r, "signal_face", None) or 0.35)
        text = r.text or ""
        words = getattr(r, "signal_words", None)
        if words is None:
            words = words_score_from_text(text)
        else:
            words = clamp01(words)
        poss = getattr(r, "possibility", None)
        if poss is None:
            poss = possibility(voice, words, face)

        sub_nodes = []
        for j, sn in enumerate(split_sub_nodes(text)):
            wj = words_score_from_text(sn)
            vj = voice
            fj = face
            pj = possibility(vj, wj, fj)
            sub_nodes.append(
                {
                    "id": f"E{event_id + 1}_S{j + 1}",
                    "text": sn[:200],
                    "voice": round(vj, 3),
                    "words": round(wj, 3),
                    "facial": round(fj, 3),
                    "possibility": round(pj, 3),
                }
            )

        event_id += 1
        temporal_boost = 0.04 if TEMPORAL.search(text) else 0.0
        events.append(
            {
                "id": f"E{event_id}",
                "order_index": getattr(r, "chunk_index", event_id - 1),
                "summary": text[:280] + ("…" if len(text) > 280 else ""),
                "voice": round(voice, 3),
                "words": round(words, 3),
                "facial": round(face, 3),
                "possibility": round(min(1.0, poss + temporal_boost), 3),
                "sub_nodes": sub_nodes,
            }
        )

    # Reconstruct: sort by possibility desc, tie-break speech order
    ranked = sorted(
        enumerate(events),
        key=lambda it: (-it[1]["possibility"], it[1]["order_index"]),
    )
    reconstructed = []
    for rank, (_, ev) in enumerate(ranked, start=1):
        reconstructed.append(
            {
                "rank": rank,
                "event_id": ev["id"],
                "summary": ev["summary"],
                "possibility": ev["possibility"],
                "confidence_band": "high" if ev["possibility"] >= 0.62 else ("mid" if ev["possibility"] >= 0.45 else "low"),
            }
        )

    return {
        "formula": f"P = {WEIGHT_VOICE}·voice + {WEIGHT_WORDS}·words + {WEIGHT_FACE}·facial",
        "weights": {"voice": WEIGHT_VOICE, "words": WEIGHT_WORDS, "facial": WEIGHT_FACE},
        "events": events,
        "reconstructed_timeline": reconstructed,
    }
