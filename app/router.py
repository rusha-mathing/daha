from fastapi import APIRouter
from app.core.router import core_router

router = APIRouter()
router.include_router(core_router)
