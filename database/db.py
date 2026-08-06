"""
Database setup for the POC.
Uses SQLite for local/POC use. Swap SQLALCHEMY_DATABASE_URL for a SQL Server
connection string (via pyodbc) for production use.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

from pathlib import Path
_db_dir = Path(__file__).resolve().parent.parent.parent / "file-classification-"
_db_dir.mkdir(parents=True, exist_ok=True)
_db_path = _db_dir / "converter.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{_db_path.as_posix()}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ConverterHistory(Base):
    __tablename__ = "converter_history"

    id = Column(Integer, primary_key=True, index=True)
    source_format = Column(String(50), nullable=False)
    target_format = Column(String(50), nullable=False)
    original_file_name = Column(String(300), nullable=True)
    converted_file_name = Column(String(300), nullable=True)
    status = Column(String(50), nullable=False)  # SUCCESS / FAILED
    error_message = Column(Text, nullable=True)
    created_by = Column(Integer, nullable=True)  # user_id
    created_date = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Create tables if they don't already exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency that yields a DB session and closes it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
