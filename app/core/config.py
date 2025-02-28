from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional

class Settings(BaseSettings):
    DB_ECHO_LOG: bool = False
    DATABASE_URL: str
    SYNC_DATABASE_URL: str

    model_config = ConfigDict(
        env_file=".env",
        extra="allow"  # 추가 필드 허용
    )

def to_camel(string: str) -> str:
    """snake_case를 camelCase로 변환합니다."""
    words = string.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])

settings = Settings()