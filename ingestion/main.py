import logging
from pathlib import Path

from ingestion.core.logging_config import setup_logging
from ingestion.persistence.db import get_session, init_db
from ingestion.persistence.repository import OfferRepository
from ingestion.pipeline.offer_ingestion_pipeline import OfferIngestionPipeline
from ingestion.pipeline.upload_htmls import upload_htmls

setup_logging()
logger = logging.getLogger(__name__)


def main(upload: bool = False):
    """
    Main function to handle the ingestion process.
    If `upload` is True, it will upload local HTML files to GCS before ingestion.
    """
    if upload:
        main_upload_htmls()
    main_ingest()


def main_upload_htmls():
    """
    Upload local HTML files to the GCS bucket.
    The HTML files should be located in the 'ingestion/data/' folder.
    """
    logger.info("☁️ Uploading HTML files to GCS...")
    upload_htmls(local_data_path_str="ingestion/data/")
    logger.info("✅ Upload completed.")


def main_ingest():
    """
    Ingest all HTML offers and populate the database.
    """
    logger.info("📥 Ingesting HTML offers...")
    init_db()

    with get_session() as session:
        repo = OfferRepository(session)
        pipeline = OfferIngestionPipeline(
            html_folder=Path("ingestion/data/"),
            repository=repo,
        )
        pipeline.run()
    logger.info("✅ Ingestion completed. Exiting")


if __name__ == "__main__":
    main()
