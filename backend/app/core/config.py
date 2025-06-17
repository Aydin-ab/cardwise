from pydantic_settings import BaseSettings, SettingsConfigDict


class BackendSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.backend")
    database_url: str = ""
    debug: bool = False
    log_level: str = "INFO"


settings = BackendSettings()
