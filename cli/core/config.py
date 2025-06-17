from pydantic_settings import BaseSettings, SettingsConfigDict


class CLISettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.cli")

    api_url: str = "http://localhost:8000/offers"


settings = CLISettings()
