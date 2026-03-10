from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Hotel WiFi SaaS"
    environment: str = "development"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60 * 24

    postgres_dsn: str = "postgresql+psycopg://hotelwifi:hotelwifi@db:5432/hotelwifi"
    redis_url: str = "redis://redis:6379/0"

    encryption_key: str = "change-me-32-byte-key-change-me-32"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
