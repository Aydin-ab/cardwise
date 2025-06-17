import logging
from typing import List

from google.cloud import storage
from google.oauth2 import service_account

from ingestion.core.config import settings

logger = logging.getLogger(__name__)


class GCSClient:
    def __init__(self):
        logger.debug("Initializing GCS client")
        credentials = service_account.Credentials.from_service_account_file(str(settings.gcs_credentials))  # type: ignore
        self.client = storage.Client(credentials=credentials)
        self.bucket = self.client.bucket(settings.gcs_bucket_name)  # type: ignore

    def list_html_files(self, prefix: str = "data/bank_htmls/") -> List[str]:
        blobs = self.client.list_blobs(self.bucket, prefix=prefix)  # type: ignore
        html_files: List[str] = [blob.name for blob in blobs if blob.name.endswith(".html")]  # type: ignore
        logger.info(f"Found {len(html_files)} HTML files in GCS under '{prefix}': {html_files}")
        return html_files

    def download_file_content(self, file_path: str) -> str:
        blob = self.bucket.blob(file_path)  # type: ignore
        logger.debug(f"Downloading HTML file content: {file_path}")
        html_doc: str = blob.download_as_text()  # type: ignore
        return html_doc
