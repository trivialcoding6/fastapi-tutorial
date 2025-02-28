import pytest
from httpx import AsyncClient
from uuid import UUID
import json

from app.models.todo import Todo

@pytest.mark.asyncio
async def test_create_todo(client: AsyncClient):
    """할 일 생성 테스트"""
    todo_data = {
        "title": "새로운 할 일",
        "content": "할 일 내용",
        "status": "NOT_STARTED"
    }
    
    response = await client.post("/api/v1/todos/", json=todo_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["content"] == todo_data["content"]
    assert data["status"] == todo_data["status"]
    assert "id" in data

@pytest.mark.asyncio
async def test_get_todo(client: AsyncClient, sample_todo: Todo):
    """할 일 조회 테스트"""
    response = await client.get(f"/api/v1/todos/{sample_todo.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(sample_todo.id)
    assert data["title"] == sample_todo.title
    assert data["content"] == sample_todo.content

@pytest.mark.asyncio
async def test_get_todos(client: AsyncClient, sample_todo: Todo):
    """할 일 목록 조회 테스트"""
    response = await client.get("/api/v1/todos/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # 상태별 필터링 테스트 - 문자열로 상태값 전달
    status_value = sample_todo.status.value  # Enum의 값을 문자열로 가져옴
    response = await client.get(f"/api/v1/todos/?status={status_value}")
    assert response.status_code == 200
    data = response.json()
    assert all(item["status"] == status_value for item in data)

@pytest.mark.asyncio
async def test_update_todo(client: AsyncClient, sample_todo: Todo):
    """할 일 업데이트 테스트"""
    update_data = {
        "title": "수정된 할 일",
        "status": "IN_PROGRESS"
    }
    
    response = await client.put(f"/api/v1/todos/{sample_todo.id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["status"] == update_data["status"]
    assert data["content"] == sample_todo.content  # 변경되지 않은 필드

@pytest.mark.asyncio
async def test_delete_todo(client: AsyncClient, sample_todo: Todo):
    """할 일 삭제 테스트"""
    response = await client.delete(f"/api/v1/todos/{sample_todo.id}")
    assert response.status_code == 204
    
    # 삭제 확인
    response = await client.get(f"/api/v1/todos/{sample_todo.id}")
    assert response.status_code == 404
