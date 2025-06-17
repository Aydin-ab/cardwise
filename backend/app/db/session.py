from typing import Generator

from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine

from backend.app.core.config import settings

_engine: Engine | None = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
        _engine = create_engine(settings.database_url, echo=settings.debug, connect_args=connect_args)
    return _engine


def get_session() -> Generator[Session, None, None]:
    """
    Yields a SQLModel session, intended for use with FastAPI Depends().
    """
    engine = get_engine()
    with Session(engine) as session:
        yield session
