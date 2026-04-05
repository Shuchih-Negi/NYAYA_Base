from sqlalchemy import Column, Float, Integer, String, Text, ForeignKey

from app.database import Base


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String(64), unique=True, nullable=False, index=True)
    counselor_name = Column(String(256), default="Sunita Sharma")
    pdf_hash = Column(String(128), nullable=True)
    verified_bns = Column(Text, default="[]")  # JSON array of section ids


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String(64), ForeignKey("cases.case_id"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    stress_label = Column(String(64), nullable=True)
    stress_score = Column(Float, nullable=True)
    signal_voice = Column(Float, nullable=True)
    signal_words = Column(Float, nullable=True)
    signal_face = Column(Float, nullable=True)
    possibility = Column(Float, nullable=True)
