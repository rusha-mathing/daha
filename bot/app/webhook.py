import logging
from fastapi import APIRouter, Request, HTTPException, status
from .models import get_users_by_difficulty_and_subject
from .bot import bot
from .config import settings
from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime

logger = logging.getLogger(__name__)

class CoursePayload(BaseModel):
    id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    start_date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    url: str = Field(..., pattern=r'^https?://.*')
    image_url: str = Field(..., pattern=r'^https?://.*')
    grades: List[int] = Field(..., min_items=1)
    difficulty: str = Field(..., min_length=1, max_length=50)
    subjects: List[str] = Field(..., min_items=1)
    organization: str = Field(..., min_length=1, max_length=100)

    @validator('grades')
    def validate_grades(cls, v):
        for grade in v:
            if not 1 <= grade <= 12:
                raise ValueError('Grades must be between 1 and 12')
        return v

    @validator('start_date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')

router = APIRouter()

@router.post("/")
async def receive_webhook(payload: CoursePayload):
    """Receive course notifications and send to matching users"""
    try:
        all_suitable_users = set()
        
        for subject in payload.subjects:
            suitable_users = await get_users_by_difficulty_and_subject(payload.difficulty, subject)
            logger.info(f"Found {len(suitable_users)} users for difficulty {payload.difficulty} and subject {subject}")
            all_suitable_users.update(suitable_users)

        if not all_suitable_users:
            logger.info(f"No suitable users found for course: {payload.title}")
            return {"message": "No suitable users found", "course_id": payload.id}

        successful_sends = 0
        failed_sends = 0
        
        for user in all_suitable_users:
            try:
                message = (
                    f"🎓 Новое по твоим интересам!\n\n"
                    f"📚 Курс: {payload.title}\n"
                    f"🔗 Ссылка: {payload.url}\n"
                    f"📅 Начало: {payload.start_date}\n\n"
                    f"{' '.join('#' + sub for sub in payload.subjects)}"
                )
                
                # Truncate message if too long
                if len(message) > settings.MAX_NOTIFICATION_LENGTH:
                    message = message[:settings.MAX_NOTIFICATION_LENGTH - 3] + "..."
                
                await bot.send_message(user.telegram_id, message)
                successful_sends += 1
                
            except Exception as e:
                logger.error(f"Failed to send message to user {user.telegram_id}: {e}")
                failed_sends += 1
        
        logger.info(f"Course {payload.id}: {successful_sends} successful, {failed_sends} failed notifications")
        
        return {
            "message": f"Notifications sent to {successful_sends} users",
            "course_id": payload.id,
            "successful_sends": successful_sends,
            "failed_sends": failed_sends,
            "total_users": len(all_suitable_users)
        }
        
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process webhook: {str(e)}"
        )
