from fastapi import APIRouter, Depends, status, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel
from typing import List

from app.dependencies import get_session
from app.auth.models import User
from app.auth.linking import linking_service
from app.core.config import settings
from app.core.user_preferences import user_preference_service
from app.core.models import CourseResponse
from app.models import Course, Subject, Difficulty, Organization, Grade
from sqlmodel import select
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/bot", tags=["Bot"])

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == settings.BOT_API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

class LinkAccountRequest(BaseModel):
    token: str
    telegram_id: int

@router.post("/link-account", status_code=status.HTTP_200_OK)
async def link_account(
    request: LinkAccountRequest,
    session: AsyncSession = Depends(get_session),
    api_key: str = Depends(get_api_key)
):
    """Link a user account with a Telegram ID."""
    user_id = await linking_service.get_user_by_link_token(session, request.token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.telegram_id = request.telegram_id
    session.add(user)
    await session.commit()

    return {"message": "Account linked successfully"}

class CoursesRequest(BaseModel):
    telegram_id: int

@router.post("/courses", response_model=List[CourseResponse])
async def get_courses_for_telegram_user(
    request: CoursesRequest,
    session: AsyncSession = Depends(get_session),
    api_key: str = Depends(get_api_key)
):
    """Get courses for a telegram user based on their preferences."""
    statement = select(User).where(User.telegram_id == request.telegram_id)
    result = await session.exec(statement)
    user = result.one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    preferences = await user_preference_service.get_preferences(session, user.id)

    query = select(Course).options(
        selectinload(Course.subjects),
        selectinload(Course.grades),
        selectinload(Course.organization),
        selectinload(Course.difficulty),
    )

    if preferences:
        if preferences.subject_ids:
            query = query.join(Course.subjects).where(Subject.id.in_(preferences.subject_ids))
        if preferences.difficulty_ids:
            query = query.join(Course.difficulty).where(Difficulty.id.in_(preferences.difficulty_ids))
        if preferences.organization_ids:
            query = query.join(Course.organization).where(Organization.id.in_(preferences.organization_ids))
        if preferences.grade_ids:
            query = query.join(Course.grades).where(Grade.id.in_(preferences.grade_ids))

    result = await session.exec(query)
    courses = result.all()
    return courses 