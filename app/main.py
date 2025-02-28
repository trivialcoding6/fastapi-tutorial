from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import router
from app.db.base import init_db
from loguru import logger
from app.core.logging import setup_logging
import asyncio
from app.core.config import settings
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status



@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 실행
    setup_logging()
    logger.info("Application starting up...")
    try:
        await init_db()
        yield
    except asyncio.CancelledError:
        logger.warning("Lifespan tasks cancelled")
    finally:
        # 종료 시 실행
        logger.info("Application shutting down...")

app = FastAPI(title="Todo API", version="1.0.0", debug=settings.DB_ECHO_LOG, lifespan=lifespan)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    요청 검증 오류를 사용자 친화적인 형식으로 변환합니다.
    """
    errors = []
    for error in exc.errors():
        error_type = error.get("type", "")
        if error_type == "json_invalid":
            errors.append({
                "message": "잘못된 JSON 형식입니다. 요청 본문을 확인해주세요.",
                "location": error.get("loc", []),
                "error_type": "invalid_json"
            })
        else:
            errors.append({
                "message": error.get("msg", "알 수 없는 오류가 발생했습니다."),
                "location": error.get("loc", []),
                "error_type": error_type
            })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"errors": errors, "success": False}
    )

app.include_router(router, prefix="/api/v1")