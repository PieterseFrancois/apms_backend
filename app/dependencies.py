from typing import Generator
from sqlalchemy.orm import Session
from .database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
