from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DB_ECHO_LOG: bool = False
    DATABASE_URL: str
    SYNC_DATABASE_URL: str

    model_config = ConfigDict(
        env_file=".env",
        extra="allow"  # 추가 필드 허용
    )

settings = Settings()