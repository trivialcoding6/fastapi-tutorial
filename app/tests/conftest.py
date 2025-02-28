import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator, Generator

from app.main import app
from app.models.base import Base
from app.db.session import get_db
from app.models.todo import Todo, TodoStatus
from app.core.config import settings
from uuid import uuid4
from datetime import datetime, timezone

# 테스트용 데이터베이스 URL (인메모리 SQLite 사용)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# 테스트용 엔진 및 세션 생성
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="session")
async def setup_database():
    """테스트 데이터베이스 설정"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(setup_database) -> AsyncGenerator[AsyncSession, None]:
    """테스트용 데이터베이스 세션 제공"""
    async with TestingSessionLocal() as session:
        yield session
        # 각 테스트 후 롤백
        await session.rollback()

@pytest.fixture
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """테스트용 API 클라이언트 제공"""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()

@pytest.fixture
async def sample_todo(db_session) -> Todo:
    """샘플 Todo 항목 생성"""
    todo = Todo(
        id=uuid4(),
        title="테스트 할 일",
        content="테스트 내용입니다",
        status=TodoStatus.NOT_STARTED,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db_session.add(todo)
    await db_session.commit()
    await db_session.refresh(todo)
    return todo
