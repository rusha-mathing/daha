from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from datetime import datetime
from typing import Dict, Any, List

from app.dependencies import get_session
from app.models import Course, Subject, Difficulty, Organization, Grade
from app.auth.models import User
from app.core.metrics import metrics

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@router.get("/health/detailed")
async def detailed_health_check(session: AsyncSession = Depends(get_session)) -> Dict[str, Any]:
    """Detailed health check with database connectivity"""
    try:
        # Test database connectivity
        result = await session.exec(select(Course).limit(1))
        db_status = "connected"
        
        # Get basic statistics
        courses_count = len(await session.exec(select(Course)).all())
        subjects_count = len(await session.exec(select(Subject)).all())
        users_count = len(await session.exec(select(User)).all())
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "database": {
                "status": db_status,
                "courses": courses_count,
                "subjects": subjects_count,
                "users": users_count
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "database": {
                "status": "disconnected",
                "error": str(e)
            }
        }

@router.get("/health/ready")
async def readiness_check(session: AsyncSession = Depends(get_session)) -> Dict[str, Any]:
    """Readiness check for Kubernetes/container orchestration"""
    try:
        # Test database connectivity
        await session.exec(select(Course).limit(1))
        
        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "not_ready",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

@router.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get application metrics"""
    return metrics.get_metrics()

@router.post("/metrics/reset")
async def reset_metrics() -> Dict[str, Any]:
    """Reset all metrics"""
    metrics.reset()
    return {"message": "Metrics reset successfully"} 