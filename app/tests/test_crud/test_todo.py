import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from datetime import datetime

from app.models.todo import Todo, TodoStatus
from app.schemas.todo import TodoCreate, TodoUpdate
from app.crud.todo import get_todo, get_todos, create_todo, update_todo, delete_todo

@pytest.mark.asyncio
async def test_create_todo(db_session: AsyncSession):
    """할 일 생성 CRUD 테스트"""
    todo_create = TodoCreate(
        title="테스트 할 일",
        content="테스트 내용",
        status=TodoStatus.TODO
    )
    
    db_todo = await create_todo(db=db_session, todo=todo_create)
    
    assert db_todo.id is not None
    assert db_todo.title == todo_create.title
    assert db_todo.content == todo_create.content
    assert db_todo.status == todo_create.status
    assert db_todo.created_at is not None
    assert db_todo.updated_at is not None

@pytest.mark.asyncio
async def test_get_todo(db_session: AsyncSession, sample_todo: Todo):
    """할 일 조회 CRUD 테스트"""
    db_todo = await get_todo(db=db_session, todo_id=sample_todo.id)
    
    assert db_todo is not None
    assert db_todo.id == sample_todo.id
    assert db_todo.title == sample_todo.title
    assert db_todo.content == sample_todo.content

@pytest.mark.asyncio
async def test_get_todos(db_session: AsyncSession, sample_todo: Todo):
    """할 일 목록 조회 CRUD 테스트"""
    todos = await get_todos(db=db_session)
    
    assert len(todos) >= 1
    assert any(todo.id == sample_todo.id for todo in todos)
    
    # 상태별 필터링 테스트
    filtered_todos = await get_todos(db=db_session, status=sample_todo.status)
    assert all(todo.status == sample_todo.status for todo in filtered_todos)

@pytest.mark.asyncio
async def test_update_todo(db_session: AsyncSession, sample_todo: Todo):
    """할 일 업데이트 CRUD 테스트"""
    todo_update = TodoUpdate(
        title="수정된 할 일",
        status=TodoStatus.IN_PROGRESS
    )
    
    updated_todo = await update_todo(db=db_session, todo_id=sample_todo.id, todo_update=todo_update)
    
    assert updated_todo is not None
    assert updated_todo.id == sample_todo.id
    assert updated_todo.title == todo_update.title
    assert updated_todo.status == todo_update.status
    assert updated_todo.content == sample_todo.content  # 변경되지 않은 필드

@pytest.mark.asyncio
async def test_delete_todo(db_session: AsyncSession, sample_todo: Todo):
    """할 일 삭제 CRUD 테스트"""
    success = await delete_todo(db=db_session, todo_id=sample_todo.id)
    
    assert success is True
    
    # 삭제 확인
    deleted_todo = await get_todo(db=db_session, todo_id=sample_todo.id)
    assert deleted_todo is None
