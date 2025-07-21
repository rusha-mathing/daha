from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.core.models import (
    SubjectResponse,
    DifficultyResponse,
    OrganizationResponse,
    GradeResponse,
    CourseResponse,
    CreateResponse,
    SubjectCreate,
    DifficultyCreate,
    OrganizationCreate,
    GradeCreate,
    CourseCreate,
)
from app.models import CourseUpdate
from app.dependencies import get_session
from app.core.services import subject_service, difficulty_service, organization_service, grade_service, course_service
from app.core.exceptions import NotFoundError, ValidationError
from app.auth.services import auth_service
from app.auth.models import User, UserRole

protected_router = APIRouter(prefix="/admin", tags=["Admin"])

@protected_router.post('/subjects/', response_model=CreateResponse, status_code=status.HTTP_201_CREATED)
async def create_subject_protected(
    subject: SubjectCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth_service.require_role(UserRole.ADMIN))
):
    """Create a new subject (admin only)"""
    try:
        db_subject = await subject_service.create(session, subject.model_dump())
        return CreateResponse(id=db_subject.id)
    except Exception as e:
        raise ValidationError(f'Failed to create subject: {str(e)}')

@protected_router.put('/subjects/{id}', response_model=SubjectResponse)
async def update_subject_protected(
    id: int,
    subject: SubjectCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth_service.require_role(UserRole.ADMIN))
):
    """Update a subject (admin only)"""
    return await subject_service.update(session, id, subject.model_dump())

@protected_router.delete('/subjects/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject_protected(
    id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth_service.require_role(UserRole.ADMIN))
):
    """Delete a subject (admin only)"""
    await subject_service.delete(session, id)

@protected_router.post('/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course_protected(
    course: CourseCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth_service.require_role(UserRole.MODERATOR))
):
    """Create a new course (moderator or admin only)"""
    try:
        if not course.subjects or len(course.subjects) == 0:
            raise ValidationError('Course must have at least one subject')
        course_data = {
            'title': course.title,
            'description': course.description,
            'start_date': course.start_date,
            'end_date': course.end_date,
            'url': course.url,
            'image_url': course.image_url,
        }
        return await course_service.create_with_relations(
            session=session,
            course_data=course_data,
            difficulty_type=course.difficulty,
            organization_name=course.organization,
            subject_types=course.subjects,
            grade_values=course.grades,
        )
    except NotFoundError:
        raise
    except Exception as e:
        raise ValidationError(f'Failed to create course: {str(e)}')

@protected_router.put('/courses/{id}', response_model=CourseResponse)
async def update_course_protected(
    id: int,
    course_update: CourseUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth_service.require_role(UserRole.MODERATOR))
):
    """Update a course (moderator or admin only)"""
    return await course_service.update_with_relations(session, id, course_update.model_dump())

@protected_router.delete('/courses/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course_protected(
    id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth_service.require_role(UserRole.ADMIN))
):
    """Delete a course (admin only)"""
    await course_service.delete(session, id)

@protected_router.get('/my-courses/', response_model=List[CourseResponse])
async def get_my_courses(
    current_user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get courses created by current user"""
    return []

@protected_router.get('/analytics/', response_model=dict)
async def get_analytics(
    current_user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get analytics (moderator or admin only)"""
    if current_user.role not in [UserRole.MODERATOR, UserRole.ADMIN]:
        raise ValidationError("Insufficient permissions")
    return {"total_courses": 0, "total_users": 0, "total_subjects": 0} 