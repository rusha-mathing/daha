import asyncio
import uvicorn
from app.main import app
from app.models import init_db

async def setup():
    await init_db()

if __name__ == "__main__":
    asyncio.run(setup())
    uvicorn.run(app, host="0.0.0.0", port=8000) 