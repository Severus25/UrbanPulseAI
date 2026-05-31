from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "development"
    log_level: str = "INFO"
    cors_origins: list[str] = ["http://localhost:3000"]

    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "urbanpulse"
    postgres_user: str = "urbanpulse"
    postgres_password: str = "changeme"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""

    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"

    # External APIs
    openweathermap_api_key: str = ""
    mapbox_access_token: str = ""

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}"
        return f"redis://{self.redis_host}:{self.redis_port}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
