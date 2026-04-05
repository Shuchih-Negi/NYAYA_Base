from typing import Any, Optional

from pydantic import BaseModel, Field


class CaseCreate(BaseModel):
    case_id: str = "DEMO-001"
    counselor_name: str = "Sunita Sharma"


class TranscriptChunkIn(BaseModel):
    text: str
    chunk_index: Optional[int] = None
    stress_label: Optional[str] = None
    stress_score: Optional[float] = None
    signal_voice: Optional[float] = Field(None, ge=0.0, le=1.0)
    signal_words: Optional[float] = Field(None, ge=0.0, le=1.0)
    signal_face: Optional[float] = Field(None, ge=0.0, le=1.0)
    possibility: Optional[float] = Field(None, ge=0.0, le=1.0)


class GuidanceRequest(BaseModel):
    transcript_window: str
    case_id: Optional[str] = None


class VerifyBnsRequest(BaseModel):
    section_ids: list[str] = Field(default_factory=list)


class TribeProxyRequest(BaseModel):
    """Optional server-side audio features; MVP often sends score from client."""
    audio_base64: Optional[str] = None
    energy_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class BrainMappingRequest(BaseModel):
    """Seed random brain panels from live modality scores."""

    voice: float = Field(0.35, ge=0.0, le=1.0)
    words: float = Field(0.45, ge=0.0, le=1.0)
    face: float = Field(0.35, ge=0.0, le=1.0)
    possibility: float = Field(0.45, ge=0.0, le=1.0)
    stress_points: list[float] = Field(default_factory=list)
    n_timesteps: int = Field(15, ge=5, le=30)


class SyntheticBrainRequest(BaseModel):
    spoken_sample: str = ""
    n_timesteps: int = Field(15, ge=5, le=30)
