from pydantic_settings import BaseSettings, SettingsConfigDict


class CLISettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.cli")

    backend_api_url: str = ""


settings = CLISettings()
