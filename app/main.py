from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import router
from app.db.base import init_db
from loguru import logger
from app.core.logging import setup_logging
import asyncio
from app.core.config import settings


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

app.include_router(router, prefix="/api/v1")