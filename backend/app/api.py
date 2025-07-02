from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.models import create_db_and_models
from app.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_models()
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, debug=True)
    app.include_router(router)
    return app
