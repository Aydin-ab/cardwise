import logging

from sqlmodel import Session, SQLModel, create_engine

from ingestion.core.config import settings

logger = logging.getLogger(__name__)

# Set connect_args only for SQLite
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

# Create the engine from settings
engine = create_engine(settings.database_url, echo=settings.log_level == "DEBUG", connect_args=connect_args)


def get_session() -> Session:
    """
    Create a new SQLModel session bound to the configured engine.
    """
    return Session(engine)


def init_db() -> None:
    """
    Create tables in the database. Should be called once at startup.
    """
    from cardwise.persistence.models.offer_db import OfferDB  # type: ignore # noqa: F401

    logger.info("Initializing database and creating tables...")
    SQLModel.metadata.create_all(engine)
