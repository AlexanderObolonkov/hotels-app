from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    REDIS_HOST: str
    REDIS_PORT: str
    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASS: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
