from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    database_url: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    openai_api_key: str = ""
    anthropic_api_key: str = ""

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
