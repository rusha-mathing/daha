from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload

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
    CourseFilters,
)
from app.models import CourseUpdate
from app.core.services import subject_service, difficulty_service, organization_service, grade_service, course_service
from app.core.exceptions import NotFoundError, DatabaseError, ValidationError
from app.dependencies import get_session
from app.models import Course, Subject, Difficulty, Organization, Grade

router = APIRouter()


# Subject endpoints
@router.get('/subjects/', response_model=List[SubjectResponse])
async def get_subjects(session: AsyncSession = Depends(get_session)):
    """Get all subjects"""
    return await subject_service.get_all(session)


@router.get('/subjects/{id}', response_model=SubjectResponse)
async def get_subject(id: int, session: AsyncSession = Depends(get_session)):
    """Get a subject by ID"""
    return await subject_service.get_by_id(session, id)


@router.post('/subjects/', response_model=CreateResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(subject: SubjectCreate, session: AsyncSession = Depends(get_session)):
    """Create a new subject"""
    try:
        db_subject = await subject_service.create(session, subject.model_dump())
        return CreateResponse(id=db_subject.id)
    except Exception as e:
        raise ValidationError(f'Failed to create subject: {str(e)}')


@router.put('/subjects/{id}', response_model=SubjectResponse)
async def update_subject(id: int, subject: SubjectCreate, session: AsyncSession = Depends(get_session)):
    """Update a subject"""
    return await subject_service.update(session, id, subject.model_dump())


@router.delete('/subjects/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(id: int, session: AsyncSession = Depends(get_session)):
    """Delete a subject"""
    await subject_service.delete(session, id)


# Difficulty endpoints
@router.get('/difficulties/', response_model=List[DifficultyResponse])
async def get_difficulties(session: AsyncSession = Depends(get_session)):
    """Get all difficulties"""
    return await difficulty_service.get_all(session)


@router.get('/difficulties/{id}', response_model=DifficultyResponse)
async def get_difficulty(id: int, session: AsyncSession = Depends(get_session)):
    """Get a difficulty by ID"""
    return await difficulty_service.get_by_id(session, id)


@router.post('/difficulties/', response_model=CreateResponse, status_code=status.HTTP_201_CREATED)
async def create_difficulty(difficulty: DifficultyCreate, session: AsyncSession = Depends(get_session)):
    """Create a new difficulty"""
    try:
        db_difficulty = await difficulty_service.create(session, difficulty.model_dump())
        return CreateResponse(id=db_difficulty.id)
    except Exception as e:
        raise ValidationError(f'Failed to create difficulty: {str(e)}')


@router.put('/difficulties/{id}', response_model=DifficultyResponse)
async def update_difficulty(id: int, difficulty: DifficultyCreate, session: AsyncSession = Depends(get_session)):
    """Update a difficulty"""
    return await difficulty_service.update(session, id, difficulty.model_dump())


@router.delete('/difficulties/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_difficulty(id: int, session: AsyncSession = Depends(get_session)):
    """Delete a difficulty"""
    await difficulty_service.delete(session, id)


# Organization endpoints
@router.get('/organizations/', response_model=List[OrganizationResponse])
async def get_organizations(session: AsyncSession = Depends(get_session)):
    """Get all organizations"""
    return await organization_service.get_all(session)


@router.get('/organizations/{id}', response_model=OrganizationResponse)
async def get_organization(id: int, session: AsyncSession = Depends(get_session)):
    """Get an organization by ID"""
    return await organization_service.get_by_id(session, id)


@router.post('/organizations/', response_model=CreateResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(organization: OrganizationCreate, session: AsyncSession = Depends(get_session)):
    """Create a new organization"""
    try:
        db_organization = await organization_service.create(session, organization.model_dump())
        return CreateResponse(id=db_organization.id)
    except Exception as e:
        raise ValidationError(f'Failed to create organization: {str(e)}')


@router.put('/organizations/{id}', response_model=OrganizationResponse)
async def update_organization(id: int, organization: OrganizationCreate, session: AsyncSession = Depends(get_session)):
    """Update an organization"""
    return await organization_service.update(session, id, organization.model_dump())


@router.delete('/organizations/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(id: int, session: AsyncSession = Depends(get_session)):
    """Delete an organization"""
    await organization_service.delete(session, id)


# Grade endpoints
@router.get('/grades/', response_model=List[GradeResponse])
async def get_grades(session: AsyncSession = Depends(get_session)):
    """Get all grades"""
    return await grade_service.get_all(session)


@router.get('/grades/{id}', response_model=GradeResponse)
async def get_grade(id: int, session: AsyncSession = Depends(get_session)):
    """Get a grade by ID"""
    return await grade_service.get_by_id(session, id)


@router.post('/grades/', response_model=CreateResponse, status_code=status.HTTP_201_CREATED)
async def create_grade(grade: GradeCreate, session: AsyncSession = Depends(get_session)):
    """Create a new grade"""
    try:
        db_grade = await grade_service.create(session, grade.model_dump())
        return CreateResponse(id=db_grade.id)
    except Exception as e:
        raise ValidationError(f'Failed to create grade: {str(e)}')


@router.put('/grades/{id}', response_model=GradeResponse)
async def update_grade(id: int, grade: GradeCreate, session: AsyncSession = Depends(get_session)):
    """Update a grade"""
    return await grade_service.update(session, id, grade.model_dump())


@router.delete('/grades/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_grade(id: int, session: AsyncSession = Depends(get_session)):
    """Delete a grade"""
    await grade_service.delete(session, id)


# Course endpoints with filtering
@router.get('/courses/', response_model=List[CourseResponse])
async def get_courses(
    filters: CourseFilters = Depends(),
    session: AsyncSession = Depends(get_session),
):
    """Get courses with filtering"""
    try:
        # Build query with filters
        query = select(Course).options(
            selectinload(Course.subjects),
            selectinload(Course.grades),
            selectinload(Course.organization),
            selectinload(Course.difficulty),
        )

        # Apply filters
        if filters.subject:
            query = query.join(Course.subjects).where(Subject.type == filters.subject)

        if filters.difficulty:
            query = query.join(Course.difficulty).where(Difficulty.type == filters.difficulty)

        if filters.organization:
            query = query.join(Course.organization).where(Organization.name == filters.organization)

        if filters.grade:
            query = query.join(Course.grades).where(Grade.grade == filters.grade)

        if filters.start_date:
            query = query.where(Course.start_date >= filters.start_date)

        if filters.end_date:
            query = query.where(Course.end_date <= filters.end_date)

        if filters.search:
            search_term = f'%{filters.search}%'
            query = query.where((Course.title.ilike(search_term)) | (Course.description.ilike(search_term)))

        # Execute query
        result = await session.exec(query)
        courses = result.all()

        return courses

    except Exception as e:
        raise DatabaseError(f'Failed to fetch courses: {str(e)}')


@router.get('/courses/{id}', response_model=CourseResponse)
async def get_course(id: int, session: AsyncSession = Depends(get_session)):
    """Get a course by ID"""
    return await course_service.get_by_id_with_relations(session, id)


@router.post('/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, session: AsyncSession = Depends(get_session)):
    """Create a new course"""
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


@router.put('/courses/{id}', response_model=CourseResponse)
async def update_course(id: int, course_update: CourseUpdate, session: AsyncSession = Depends(get_session)):
    """Update a course"""
    return await course_service.update_with_relations(session, id, course_update)


@router.delete('/courses/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(id: int, session: AsyncSession = Depends(get_session)):
    """Delete a course"""
    await course_service.delete(session, id)
