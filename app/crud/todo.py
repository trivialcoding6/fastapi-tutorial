from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.future import select
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional, List

from app.models.todo import Todo, TodoStatus
from app.schemas.todo import TodoCreate, TodoUpdate

async def get_todo(db: AsyncSession, todo_id: UUID) -> Optional[Todo]:
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    return result.scalars().one_or_none()

async def get_todos(
    db: AsyncSession,
    status: Optional[TodoStatus] = None
) -> List[Todo]:
    query = select(Todo)
    
    if status:
        query = query.where(Todo.status == status)
    
    result = await db.execute(query)
    return result.scalars().all()

async def create_todo(db: AsyncSession, todo: TodoCreate) -> Todo:
    db_todo = Todo(
        title=todo.title,
        content=todo.content,
        status=todo.status,
        start_date=todo.start_date,
        end_date=todo.end_date
    )
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

async def update_todo(
    db: AsyncSession, 
    todo_id: UUID, 
    todo_update: TodoUpdate
) -> Optional[Todo]:
    db_todo = await get_todo(db, todo_id)
    if not db_todo:
        return None
    
    update_data = todo_update.model_dump(exclude_unset=True)
    
    # 업데이트 시간 자동 설정
    update_data["updated_at"] = datetime.now(timezone.utc).replace(tzinfo=None)
    
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

async def delete_todo(db: AsyncSession, todo_id: UUID) -> bool:
    db_todo = await get_todo(db, todo_id)
    if not db_todo:
        return False
    
    await db.delete(db_todo)
    await db.commit()
    return True
