from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, DateTime
from datetime import datetime, timezone
from uuid import UUID, uuid4
from app.models.base import Base

class TodoStatus(Enum):
    NOT_STARTED = "NOT_STARTED"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(String(255))
    status: Mapped[TodoStatus] = mapped_column(Enum(TodoStatus))
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
    