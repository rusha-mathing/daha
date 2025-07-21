from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import create_db_and_models
from app.core.router import router as core_router
from app.core.health import router as health_router
from app.auth.router import router as auth_router
from app.bot.router import router as bot_router
from app.core.middleware import LoggingMiddleware, ErrorHandlingMiddleware
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Starting application...')
    await create_db_and_models()
    logger.info('Database initialized successfully')
    yield
    logger.info('Shutting down application...')


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description='API for managing courses, subjects, and educational resources',
        version='1.0.0',
        lifespan=lifespan,
        debug=settings.DEBUG,
    )

    # Add middleware
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)

    # Add CORS middleware with configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        allow_headers=['*'],
    )

    # Include routers
    app.include_router(core_router)
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(bot_router)

    return app
