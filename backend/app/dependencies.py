from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession
from app.models import engine

async def get_session() -> AsyncGenerator[SQLModelAsyncSession, None]:
    async with SQLModelAsyncSession(bind=engine, expire_on_commit=False) as session:
        yield session 