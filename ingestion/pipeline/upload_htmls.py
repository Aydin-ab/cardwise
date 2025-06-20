# Upload to GCS Bucket if data in data/ folder is present here
import logging
from pathlib import Path

from ingestion.gcs.gcs_client import GCSClient

logger = logging.getLogger(__name__)


def upload_htmls(local_data_path_str: str) -> None:
    """
    Upload HTML files from the local 'data/' folder to a GCS bucket.
    Returns:
        List of (bank_id, file_name) tuples for uploaded files.
    """
    gcs = GCSClient()
    local_data_path = Path(local_data_path_str)
    if not local_data_path.exists():
        logger.error(f"Local data path '{local_data_path}' does not exist.")
        return
    if not local_data_path.is_dir():
        logger.error(f"Local data path '{local_data_path}' is not a directory.")
        return
    for file_path in local_data_path.glob("*.html"):
        logger.info(f"Found: {file_path}")
        if not file_path.is_file():
            logger.warning(f"Skipping non-file path: {file_path}")
            continue
        try:
            gcs.upload_file(str(file_path))
        except Exception as e:
            logger.error(f"Failed to upload {file_path}: {e}")
