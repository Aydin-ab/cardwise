from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class BackendSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.ingestion")
    database_url: str = ""
    log_level: str = "INFO"
    gcs_credentials: Path = Path("ingestion/gcs/ingestion-bot-key.json")
    gcs_bucket_name: str = "cardwise-html-private"


settings = BackendSettings()
