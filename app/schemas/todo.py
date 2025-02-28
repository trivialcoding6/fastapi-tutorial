from app.schemas.base import CamelBaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import model_validator

# TodoStatus Enum 정의 - 모델과 일치시킴
class TodoStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

# 기본 Todo 스키마
class TodoBase(CamelBaseModel):
    title: str
    content: str

# Todo 생성 시 사용할 스키마
class TodoCreate(TodoBase):
    status: TodoStatus = TodoStatus.NOT_STARTED
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
    @model_validator(mode='after')
    def validate_dates(self) -> 'TodoCreate':
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("종료 날짜는 시작 날짜 이후여야 합니다")
        return self

# Todo 업데이트 시 사용할 스키마 (모든 필드 선택적)
class TodoUpdate(CamelBaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[TodoStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
    @model_validator(mode='after')
    def check_at_least_one_field(self) -> 'TodoUpdate':
        values = {k: v for k, v in self.__dict__.items() if v is not None}
        if not values:
            raise ValueError("최소한 하나 이상의 필드가 제공되어야 합니다")
        return self

# 데이터베이스에서 가져온 Todo 정보를 반환할 스키마
class Todo(CamelBaseModel):
    id: UUID
    title: str
    content: str
    status: TodoStatus
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
