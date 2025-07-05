from fastapi import APIRouter
from app.core.improved_router import improved_router

router = APIRouter()
router.include_router(improved_router)
