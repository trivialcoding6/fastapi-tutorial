from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from datetime import datetime, timezone
from uuid import uuid4
from app.models.base import Base
from typing import Optional
from enum import Enum as PyEnum

class TodoStatus(str, PyEnum):
    NOT_STARTED = "NOT_STARTED"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[PgUUID] = mapped_column(PgUUID, primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(String(255))
    status: Mapped[TodoStatus] = mapped_column(Enum(TodoStatus), default=TodoStatus.NOT_STARTED)

    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
    