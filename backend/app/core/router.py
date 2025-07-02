from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.models import CourseResponse, SubjectResponse, OrganizationResponse, GradeResponse, DifficultyResponse
from app.models import get_session, Course, Subject, Organization, Grade, Difficulty
from app.core.models import (
    CreateResponse,
)
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


@core_router.post('/subjects/', response_model=CreateResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(subject: SubjectCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_subject = Subject(**subject.model_dump(exclude_unset=True))
        session.add(db_subject)
        await session.commit()
        await session.refresh(db_subject)
        return CreateResponse(id=db_subject.id)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@core_router.post('/difficulties/', response_model=CreateResponse, status_code=status.HTTP_201_CREATED)
async def create_difficulty(difficulty: DifficultyCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_difficulty = Difficulty(**difficulty.model_dump(exclude_unset=True))
        session.add(db_difficulty)
        await session.commit()
        await session.refresh(db_difficulty)
        return db_difficulty
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.post('/organizations/', response_model=CreateResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(organization: OrganizationCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_organization = Organization(**organization.model_dump(exclude_unset=True))
        session.add(db_organization)
        await session.commit()
        await session.refresh(db_organization)
        return db_organization
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.post('/grades/', response_model=CreateResponse, status_code=status.HTTP_201_CREATED)
async def create_grade(grade: GradeCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_grade = Grade(**grade.model_dump(exclude_unset=True))
        session.add(db_grade)
        await session.commit()
        await session.refresh(db_grade)
        return db_grade
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.post('/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_difficulty = (await session.exec(select(Difficulty).where(Difficulty.type == course.difficulty))).first()
        if not db_difficulty:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Difficulty not found')

        db_organization = (
            await session.exec(select(Organization).where(Organization.name == course.organization))
        ).first()
        if not db_organization:
            db_organization = Organization(name=course.organization)
            session.add(db_organization)
            await session.commit()
            await session.refresh(db_organization)

        db_subjects = []
        for subject_type in course.subjects:
            db_subject = (await session.exec(select(Subject).where(Subject.type == subject_type))).first()
            if not db_subject:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Subject {subject_type} not found')
            db_subjects.append(db_subject)

        if not db_subjects:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Course must have at least one subject')

        db_grades = []
        for grade_value in course.grades:
            db_grade = (await session.exec(select(Grade).where(Grade.grade == grade_value))).first()
            if not db_grade:
                db_grade = Grade(grade=grade_value)
                session.add(db_grade)
                await session.commit()
                await session.refresh(db_grade)
            db_grades.append(db_grade)

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
            course_grade_link = CourseGradeLink(course_id=db_course.id, grade_id=grade.id)  # Corrected
            session.add(course_grade_link)

        await session.commit()
        result = await session.exec(
            select(Course)
            .where(Course.id == db_course.id)
            .options(
                selectinload(Course.subjects),
                selectinload(Course.grades),
                selectinload(Course.organization),
                selectinload(Course.difficulty),
            )
        )
        db_course = result.first()

        return db_course

    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.put('/subjects/{id}', response_model=CreateResponse)
async def update_subject(id: int, subject: SubjectCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_subject = await session.get(Subject, id)
        if not db_subject:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Subject not found')

        subject_data = subject.model_dump(exclude_unset=True)
        for key, value in subject_data.items():
            setattr(db_subject, key, value)

        session.add(db_subject)
        await session.commit()
        await session.refresh(db_subject)
        return db_subject
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.put('/difficulties/{id}', response_model=CreateResponse)
async def update_difficulty(id: int, difficulty: DifficultyCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_difficulty = await session.get(Difficulty, id)
        if not db_difficulty:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Difficulty not found')

        difficulty_data = difficulty.model_dump(exclude_unset=True)
        for key, value in difficulty_data.items():
            setattr(db_difficulty, key, value)

        session.add(db_difficulty)
        await session.commit()
        await session.refresh(db_difficulty)
        return db_difficulty
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.put('/organizations/{id}', response_model=CreateResponse)
async def update_organization(id: int, organization: OrganizationCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_organization = await session.get(Organization, id)
        if not db_organization:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Organization not found')

        organization_data = organization.model_dump(exclude_unset=True)
        for key, value in organization_data.items():
            setattr(db_organization, key, value)

        session.add(db_organization)
        await session.commit()
        await session.refresh(db_organization)
        return db_organization
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.put('/grades/{id}', response_model=CreateResponse)
async def update_grade(id: int, grade: GradeCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_grade = await session.get(Grade, id)
        if not db_grade:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Grade not found')

        grade_data = grade.model_dump(exclude_unset=True)
        for key, value in grade_data.items():
            setattr(db_grade, key, value)

        session.add(db_grade)
        await session.commit()
        await session.refresh(db_grade)
        return db_grade
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.put('/courses/{id}', response_model=CourseResponse)
async def update_course(id: int, course_update: CourseCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_course = await session.get(Course, id)
        if not db_course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')

        course_data = course_update.model_dump(exclude_unset=True)
        for key, value in course_data.items():
            if key not in ['subjects', 'grades', 'organization_id', 'difficulty_id', 'subject_ids', 'grade_ids']:
                setattr(db_course, key, value)

        if course_update.organization_id is not None:
            db_organization = await session.get(Organization, course_update.organization_id)
            if not db_organization:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Organization not found')
            db_course.organization = db_organization

        if course_update.difficulty_id is not None:
            db_difficulty = await session.get(Difficulty, course_update.difficulty_id)
            if not db_difficulty:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Difficulty not found')
            db_course.difficulty = db_difficulty

        if course_update.subject_ids is not None:
            db_subjects = await session.exec(select(Subject).where(Subject.id.in_(course_update.subject_ids)))
            db_subjects = db_subjects.scalars().all()
            if len(db_subjects) != len(course_update.subject_ids):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='One or more subjects not found')
            db_course.subjects.clear()
            for subject in db_subjects:
                db_course.subjects.append(subject)

        if course_update.grade_ids is not None:
            db_grades = await session.exec(select(Grade).where(Grade.id.in_(course_update.grade_ids)))
            db_grades = db_grades.scalars().all()
            if len(db_grades) != len(course_update.grade_ids):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='One or more grades not found')
            db_course.grades.clear()
            for grade in db_grades:
                db_course.grades.append(grade)

        session.add(db_course)
        await session.commit()
        await session.refresh(db_course)
        return db_course
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.delete('/difficulties/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_difficulty(id: int, session: AsyncSession = Depends(get_session)):
    try:
        db_difficulty = await session.get(Difficulty, id)
        if not db_difficulty:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Difficulty not found')

        await session.delete(db_difficulty)
        await session.commit()
        return
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.delete('/organizations/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(id: int, session: AsyncSession = Depends(get_session)):
    try:
        db_organization = await session.get(Organization, id)
        if not db_organization:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Organization not found')

        await session.delete(db_organization)
        await session.commit()
        return
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.delete('/grades/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_grade(id: int, session: AsyncSession = Depends(get_session)):
    try:
        db_grade = await session.get(Grade, id)
        if not db_grade:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Grade not found')

        await session.delete(db_grade)
        await session.commit()
        return
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.delete('/courses/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(id: int, session: AsyncSession = Depends(get_session)):
    try:
        db_course = await session.get(Course, id)
        if not db_course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')

        await session.delete(db_course)
        await session.commit()
        return
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.delete('/subjects/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(id: int, session: AsyncSession = Depends(get_session)):
    try:
        db_subject = await session.get(Subject, id)
        if not db_subject:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Subject not found')

        await session.delete(db_subject)
        await session.commit()
        return
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
