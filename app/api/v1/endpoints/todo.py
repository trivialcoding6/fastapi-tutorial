from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
import logging

from app.schemas.todo import Todo as TodoSchema, TodoCreate, TodoUpdate, TodoStatus
from app.crud.todo import (
    get_todo,
    get_todos,
    create_todo,
    update_todo,
    delete_todo
)
from app.db.session import get_db

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=TodoSchema, status_code=status.HTTP_201_CREATED)
async def create_new_todo(
    todo: TodoCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    새로운 할 일 항목을 생성합니다.
    
    - **title**: 할 일 제목 (필수)
    - **content**: 할 일 내용 (필수)
    - **status**: 할 일 상태 (선택, 기본값: NOT_STARTED)
    - **start_date**: 시작 날짜 (선택)
    - **end_date**: 종료 날짜 (선택)
    """
    try:
        db_todo = await create_todo(db=db, todo=todo)
        return TodoSchema.model_validate(db_todo)
    except Exception as e:
        logger.error(f"할 일 생성 중 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="할 일 생성 중 오류가 발생했습니다"
        )

@router.get("/{todo_id}", response_model=TodoSchema)
async def read_todo(
    todo_id: UUID = Path(..., description="조회할 할 일의 ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    ID로 특정 할 일 항목을 조회합니다.
    """
    try:
        db_todo = await get_todo(db=db, todo_id=todo_id)
        if db_todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID가 {todo_id}인 할 일을 찾을 수 없습니다"
            )
        return TodoSchema.model_validate(db_todo)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"할 일 조회 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/", response_model=List[TodoSchema])
async def read_todos(
    status_filter: Optional[TodoStatus] = Query(None, alias="status", description="할 일 상태로 필터링"),
    db: AsyncSession = Depends(get_db)
):
    """
    모든 할 일 항목을 조회합니다. 선택적으로 상태별로 필터링할 수 있습니다.
    """
    try:
        db_todos = await get_todos(db=db, status=status_filter)
        # SQLAlchemy 모델을 Pydantic 모델로 변환
        return [TodoSchema.model_validate(todo) for todo in db_todos]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"할 일 목록 조회 중 오류가 발생했습니다: {str(e)}"
        )

@router.put("/{todo_id}", response_model=TodoSchema)
async def update_existing_todo(
    todo_id: UUID = Path(..., description="업데이트할 할 일의 ID"),
    todo_update: TodoUpdate = ...,
    db: AsyncSession = Depends(get_db)
):
    """
    기존 할 일 항목을 업데이트합니다.
    
    모든 필드는 선택적이며, 제공된 필드만 업데이트됩니다.
    """
    try:
        db_todo = await update_todo(db=db, todo_id=todo_id, todo_update=todo_update)
        if db_todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID가 {todo_id}인 할 일을 찾을 수 없습니다"
            )
        return TodoSchema.model_validate(db_todo)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"할 일 업데이트 중 오류가 발생했습니다: {str(e)}"
        )

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_todo(
    todo_id: UUID = Path(..., description="삭제할 할 일의 ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    할 일 항목을 삭제합니다.
    """
    try:
        success = await delete_todo(db=db, todo_id=todo_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID가 {todo_id}인 할 일을 찾을 수 없습니다"
            )
        return None  # 204 No Content 응답에는 본문이 없습니다
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"할 일 삭제 중 오류가 발생했습니다: {str(e)}"
        )
