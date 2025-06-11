import logging
import os
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

logger = logging.getLogger(__name__)

DB_PATH = Path.home() / ".cardwise" / "offers.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
DB_URL = os.getenv("CARDWISE_DATABASE_URL", f"sqlite:///{DB_PATH}")
logger.debug(f"Using database URL: {DB_URL}")
logger.debug("Creating SQLite database path if it doesn't exist")
engine = create_engine(DB_URL, echo=False)
logger.debug("SQLite database engine created")


def init_db():
    logger.info(f"Initializing SQLite database engine at {DB_URL}")
    SQLModel.metadata.create_all(engine)
    logger.info("SQLite database initialized")


def drop_db():
    logger.info(f"Dropping SQLite database at {DB_URL}")
    SQLModel.metadata.drop_all(engine)
    logger.info("SQLite database dropped")


def get_session() -> Session:
    """Get a new SQLModel session."""
    logger.debug("Creating a new SQLModel session")
    return Session(engine)
