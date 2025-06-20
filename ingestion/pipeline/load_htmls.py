import logging
from typing import List, Tuple

from ingestion.gcs.gcs_client import GCSClient

logger = logging.getLogger(__name__)


def load_htmls() -> List[Tuple[str, str]]:
    """
    Load HTML files from a private GCS bucket.
    Returns:
        List of (bank_id, html_content)
    """
    gcs = GCSClient()
    html_files = gcs.list_html_files()

    results: List[Tuple[str, str]] = []

    for file_name in html_files:
        # Retrieve bank id assuming the file name format is 'data/bank_htmls/{bank_id}.html'
        bank_id = file_name.split("/")[-1].split(".")[0]
        html_content = gcs.download_file_content(file_name)
        results.append((bank_id, html_content))
        logger.debug(f"Loaded HTML for bank '{bank_id}' from GCS")

    return results
