import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nyaya.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _sqlite_add_columns():
    if not str(engine.url).startswith("sqlite"):
        return
    from sqlalchemy import text

    with engine.begin() as conn:
        rows = conn.execute(text("PRAGMA table_info(transcripts)")).fetchall()
        names = {r[1] for r in rows}
        alters = [
            ("signal_voice", "FLOAT"),
            ("signal_words", "FLOAT"),
            ("signal_face", "FLOAT"),
            ("possibility", "FLOAT"),
        ]
        for col, typ in alters:
            if col not in names:
                conn.execute(text(f"ALTER TABLE transcripts ADD COLUMN {col} {typ}"))


def init_db():
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _sqlite_add_columns()
