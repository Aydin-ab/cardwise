import logging
from pathlib import Path

from ingestion.core.logging_config import setup_logging
from ingestion.persistence.db import get_session, init_db
from ingestion.persistence.repository import OfferRepository
from ingestion.pipeline.offer_ingestion_pipeline import OfferIngestionPipeline

setup_logging()
logger = logging.getLogger(__name__)


def main():
    init_db()

    with get_session() as session:
        repo = OfferRepository(session)
        pipeline = OfferIngestionPipeline(
            html_folder=Path("ingestion/data/"),
            repository=repo,
        )
        pipeline.run()


if __name__ == "__main__":
    main()
