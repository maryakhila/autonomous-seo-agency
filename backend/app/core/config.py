
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI SEO Agency"
    environment: str = "development"
    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/seo_agency"
    )
    secret_key: str = "change-this-before-deployment"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
