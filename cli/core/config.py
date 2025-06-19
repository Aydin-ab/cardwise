from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class CLISettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.cli")

    backend_api_url: str = ""
    database_url: str = ""
    log_level: str = "INFO"
    gcs_credentials: Path = Path("ingestion/gcs/ingestion-bot-key.json")
    gcs_bucket_name: str = "cardwise-html-private"


settings = CLISettings()
