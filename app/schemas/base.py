from pydantic import BaseModel, ConfigDict
from app.core.config import to_camel

class CamelBaseModel(BaseModel):
    """모든 스키마의 기본 클래스로, camelCase 변환을 적용합니다."""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel
    )