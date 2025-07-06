from fastapi import APIRouter, Request
from models import get_users_by_difficulty_and_subject
from bot import bot
from pydantic import BaseModel
from typing import List

class CoursePayload(BaseModel):
    id: int
    title: str
    description: str
    start_date: str
    url: str
    image_url: str
    grades: List[int]
    difficulty: str
    subjects: List[str]
    organization: str


router = APIRouter()

@router.post("/")
async def receive_webhook(payload: CoursePayload):
    all_suitable_users = set()
    for subject in payload.subjects:
        suitable_users = await get_users_by_difficulty_and_subject(payload.difficulty, subject)
        print(suitable_users)
        all_suitable_users.update(suitable_users)

    for user in all_suitable_users:
        try:
            await bot.send_message(
                user.telegram_id,
                f"Новое по твоим интересам!\n\n"
                f"Курс - {payload.title}\n"
                f"Ссылка - {payload.url}\n\n"
                f"{' '.join('#' + sub for sub in payload.subjects)}"
            )
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user.telegram_id}: {e}")
