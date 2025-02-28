from fastapi import APIRouter

router = APIRouter()

@router.get("/todos")
async def get_todos():
    return {"message": "Hello, World!"}