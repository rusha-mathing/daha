from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.models import CourseResponse, SubjectResponse, OrganizationResponse, GradeResponse, DifficultyResponse
from app.models import get_session, Course, Subject, Organization, Grade, Difficulty
from app.core.models import CourseCreateResponse, OrganizationCreateResponse, GradeCreateResponse, DifficultyCreateResponse, SubjectCreateResponse
from app.core.models import CourseCreate, OrganizationCreate, GradeCreate, DifficultyCreate, SubjectCreate
from app.models import CourseGradeLink, CourseSubjectLink

core_router = APIRouter()


@core_router.get('/subjects/', response_model=List[SubjectResponse])
async def get_subjects(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Subject))
    return result.all()


@core_router.get('/subjects/{id}', response_model=SubjectResponse)
async def get_subject(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Subject).where(Subject.id == id))
    subject = result.first()
    if not subject:
        raise HTTPException(status_code=404, detail='Subject not found')
    return subject


@core_router.get('/difficulties/', response_model=List[DifficultyResponse])
async def get_difficulties(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Difficulty))
    return result.all()


@core_router.get('/difficulties/{id}', response_model=DifficultyResponse)
async def get_difficulty(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Difficulty).where(Difficulty.id == id))
    difficulty = result.first()
    if not difficulty:
        raise HTTPException(status_code=404, detail='Difficulty not found')
    return difficulty


@core_router.get('/organizations/', response_model=List[OrganizationResponse])
async def get_organizations(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Organization))
    return result.all()


@core_router.get('/organizations/{id}', response_model=OrganizationResponse)
async def get_organization(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Organization).where(Organization.id == id))
    organization = result.first()
    if not organization:
        raise HTTPException(status_code=404, detail='Organization not found')
    return organization


@core_router.get('/grades/', response_model=List[GradeResponse])
async def get_grades(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Grade))
    return result.all()


@core_router.get('/grades/{id}', response_model=GradeResponse)
async def get_grade(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Grade).where(Grade.id == id))
    grade = result.first()
    if not grade:
        raise HTTPException(status_code=404, detail='Grade not found')
    return grade


@core_router.get('/courses/', response_model=List[CourseResponse])
async def get_courses(session: AsyncSession = Depends(get_session)):
    result = await session.exec(
        select(Course).options(
            selectinload(Course.subjects),
            selectinload(Course.grades),
            selectinload(Course.organization),
            selectinload(Course.difficulty),
        )
    )
    return result.all()


@core_router.get('/courses/{id}', response_model=CourseResponse)
async def get_course(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(
        select(Course)
        .where(Course.id == id)
        .options(
            selectinload(Course.subjects),
            selectinload(Course.grades),
            selectinload(Course.organization),
            selectinload(Course.difficulty),
        )
    )
    course = result.first()
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


@core_router.post('/subjects/', response_model=SubjectCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(subject: SubjectCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_subject = Subject(**subject.model_dump(exclude_unset=True))
        session.add(db_subject)
        await session.commit()
        await session.refresh(db_subject)
        return SubjectCreateResponse(id=db_subject.id)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


core_router.post('/difficulties/', response_model=DifficultyCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_difficulty(difficulty: DifficultyCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_difficulty = Difficulty(**difficulty.model_dump(exclude_unset=True))
        session.add(db_difficulty)
        await session.commit()
        await session.refresh(db_difficulty)
        return DifficultyCreateResponse(id=db_difficulty.id)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.post('/organizations/', response_model=OrganizationCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(organization: OrganizationCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_organization = Organization(**organization.model_dump(exclude_unset=True))
        session.add(db_organization)
        await session.commit()
        await session.refresh(db_organization)
        return OrganizationCreateResponse(id=db_organization.id)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.post('/grades/', response_model=GradeCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_grade(grade: GradeCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_grade = Grade(**grade.model_dump(exclude_unset=True))
        session.add(db_grade)
        await session.commit()
        await session.refresh(db_grade)
        return GradeCreateResponse(id=db_grade.id)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@core_router.post('/courses/', response_model=CourseCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_difficulty = await session.get(Difficulty, course.difficulty_id)
        db_organization = await session.get(Organization, course.organization_id)
        db_subjects = await session.execute(select(Subject).where(Subject.id.in_(course.subject_ids)))
        db_grades = await session.execute(select(Grade).where(Grade.id.in_(course.grade_ids)))
        db_subjects = db_subjects.scalars().all() 
        db_grades = db_grades.scalars().all()

        if not db_difficulty:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Difficulty not found")
        if not db_organization:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization not found")
        if len(db_subjects) != len(course.subject_ids):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One or more subjects not found")
        if len(db_grades) != len(course.grade_ids):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One or more grades not found")

        db_course = Course(
            title=course.title,
            description=course.description,
            start_date=course.start_date,
            end_date=course.end_date,
            url=course.url,
            image_url=course.image_url,
            organization=db_organization,
            difficulty=db_difficulty,
        )

        session.add(db_course)
        await session.commit()
        await session.refresh(db_course)

        for subject in db_subjects:
            course_subject_link = CourseSubjectLink(course_id=db_course.id, subject_id=subject.id)
            session.add(course_subject_link)

        for grade in db_grades:
            course_grade_link = CourseGradeLink(course_id=db_course.id, grade_id=grade.id)
            session.add(course_grade_link)

        await session.commit()

        return CourseCreateResponse(id=db_course.id)

    except HTTPException as e:
        await session.rollback()
        raise e  
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))