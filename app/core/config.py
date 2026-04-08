from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str

    bot_api_base_url: str = "http://localhost:8001"

    google_credentials_path: str = "app/credentials/credentials.json"
    google_token_path: str = "app/credentials/token.json"
    google_calendar_id: str = "primary"
    google_timezone: str = "Europe/Warsaw"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()