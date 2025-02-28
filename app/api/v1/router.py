from fastapi import APIRouter
from app.api.v1.endpoints import todo
router = APIRouter()

router.include_router(
    todo.router,
    tags=["todo"],
    prefix="/todos"
)
