from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from .models import get_subjects_by_telegram_id, get_difficulties_by_telegram_id, get_total_users
from .daha_api import fetch_subjects, fetch_difficulties, fetch_courses
import asyncio

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str

class UserPreferences(BaseModel):
    telegram_id: int
    subjects: List[str]
    difficulties: List[str]

class StatsResponse(BaseModel):
    total_users: int
    total_subjects: int
    total_difficulties: int
    total_courses: int

@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    import datetime
    return HealthResponse(
        status="healthy",
        message="Bot is running",
        timestamp=datetime.datetime.now().isoformat()
    )

@router.get("/stats")
async def get_stats():
    """Get bot statistics"""
    try:
        subjects = await fetch_subjects()
        difficulties = await fetch_difficulties()
        courses = await fetch_courses()
        
        total_users = await get_total_users()
        return StatsResponse(
            total_users=total_users,
            total_subjects=len(subjects) if subjects else 0,
            total_difficulties=len(difficulties) if difficulties else 0,
            total_courses=len(courses) if courses else 0
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

@router.get("/subjects")
async def get_subjects():
    """Get all available subjects"""
    try:
        subjects = await fetch_subjects()
        return {"subjects": subjects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching subjects: {str(e)}")

@router.get("/difficulties")
async def get_difficulties():
    """Get all available difficulties"""
    try:
        difficulties = await fetch_difficulties()
        return {"difficulties": difficulties}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching difficulties: {str(e)}")

@router.get("/courses")
async def get_courses():
    """Get all available courses"""
    try:
        courses = await fetch_courses()
        return {"courses": courses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching courses: {str(e)}")

@router.get("/user/{telegram_id}/preferences")
async def get_user_preferences(telegram_id: int):
    """Get user preferences by telegram ID"""
    try:
        subjects = await get_subjects_by_telegram_id(telegram_id)
        difficulties = await get_difficulties_by_telegram_id(telegram_id)
        
        return UserPreferences(
            telegram_id=telegram_id,
            subjects=subjects,
            difficulties=difficulties
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user preferences: {str(e)}")

@router.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Daha Bot API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "stats": "/stats",
            "subjects": "/subjects",
            "difficulties": "/difficulties",
            "courses": "/courses",
            "user_preferences": "/user/{telegram_id}/preferences",
            "webhook": "/webhook/"
        }
    } 