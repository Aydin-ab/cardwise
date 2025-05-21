from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

DB_PATH = Path.home() / ".cardwise" / "offers.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


def drop_db():
    SQLModel.metadata.drop_all(engine)


def get_session() -> Session:
    return Session(engine)
