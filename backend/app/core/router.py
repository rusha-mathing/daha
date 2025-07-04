from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.models import CourseResponse, SubjectResponse, OrganizationResponse, GradeResponse, DifficultyResponse
from app.models import (
    get_session,
    Course,
    Subject,
    Organization,
    Grade,
    Difficulty,
    SubjectUpdate,
    DifficultyUpdate,
    CourseUpdate,
)
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
            course_grade_link = CourseGradeLink(course_id=db_course.id, grade_id=grade.id)
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


@core_router.put('/subjects/{id}', response_model=SubjectResponse)
async def update_subject(id: int, subject: SubjectUpdate, session: AsyncSession = Depends(get_session)):
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
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_SERVER_ERROR, detail=str(e))


@core_router.put('/difficulties/{id}', response_model=DifficultyResponse)
async def update_difficulty(id: int, difficulty: DifficultyUpdate, session: AsyncSession = Depends(get_session)):
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
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.put('/organizations/{id}', response_model=OrganizationResponse)
async def update_organization(id: int, organization: OrganizationCreate, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.exec(select(Organization).where(Organization.id == id))
        db_organization = result.first()
        if not db_organization:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Organization not found')

        db_organization.name = organization.name

        session.add(db_organization)
        await session.commit()
        await session.refresh(db_organization)
        return db_organization
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.put('/grades/{id}', response_model=GradeResponse)
async def update_grade(id: int, grade: GradeCreate, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.exec(select(Grade).where(Grade.id == id))
        db_grade = result.first()
        if not db_grade:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Grade not found')

        db_grade.grade = grade.grade

        session.add(db_grade)
        await session.commit()
        await session.refresh(db_grade)
        return db_grade
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.put('/courses/{id}', response_model=CourseResponse)
async def update_course(id: int, course_update: CourseUpdate, session: AsyncSession = Depends(get_session)):
    try:
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
        db_course = result.first()
        if not db_course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')
        db_course.title = course_update.title
        db_course.description = course_update.description
        db_course.start_date = course_update.start_date
        db_course.end_date = course_update.end_date
        db_course.url = course_update.url
        db_course.image_url = course_update.image_url
        if course_update.difficulty:
            difficulty_result = await session.exec(
                select(Difficulty).where(Difficulty.type == course_update.difficulty)
            )
            db_difficulty = difficulty_result.first()
            if not db_difficulty:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Difficulty not found')
            db_course.difficulty = db_difficulty
        if course_update.subjects:
            if isinstance(course_update.subjects, str):
                subject_result = await session.exec(select(Subject).where(Subject.type == course_update.subjects))
                db_subject = subject_result.first()
                if not db_subject:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=f'Subject "{course_update.subjects}" not found'
                    )
                db_course.subjects = db_subject

            elif isinstance(course_update.subjects, list):
                subject_result = await session.exec(select(Subject).where(Subject.type.in_(course_update.subjects)))
                db_subjects = subject_result.all()

                if len(db_subjects) != len(course_update.subjects):
                    found_types = [s.type for s in db_subjects]
                    missing_subjects = [s for s in course_update.subjects if s not in found_types]
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=f'Subjects not found: {missing_subjects}'
                    )

                db_course.subjects = db_subjects
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Invalid subjects format. Must be a string or a list of strings.',
                )

        if course_update.organization:
            org_result = await session.exec(select(Organization).where(Organization.name == course_update.organization))
            db_organization = org_result.first()
            if not db_organization:
                db_organization = Organization(name=course_update.organization)
                session.add(db_organization)
                await session.commit()
                await session.refresh(db_organization)
            db_course.organization = db_organization

        if course_update.grades:
            db_grades = []
            for grade_value in course_update.grades:
                grade_result = await session.exec(select(Grade).where(Grade.grade == grade_value))
                db_grade = grade_result.first()
                if not db_grade:
                    db_grade = Grade(grade=grade_value)
                    session.add(db_grade)
                    await session.commit()
                    await session.refresh(db_grade)
                db_grades.append(db_grade)

            db_course.grades.clear()
            db_course.grades.extend(db_grades)
        session.add(db_course)
        await session.commit()
        return (
            await session.exec(
                select(Course)
                .where(Course.id == id)
                .options(
                    selectinload(Course.subjects),
                    selectinload(Course.grades),
                    selectinload(Course.organization),
                    selectinload(Course.difficulty),
                )
            )
        ).first()
    except HTTPException as e:
        await session.rollback()
        print(f'Exception caught: {e.__class__.__name__} {e}')
        raise e
    except Exception as e:
        await session.rollback()
        print(f'Exception caught: {e.__class__.__name__} {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.delete('/difficulties/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_difficulty(id: int, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.exec(select(Difficulty).where(Difficulty.id == id))
        db_difficulty = result.first()
        if not db_difficulty:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Difficulty not found')

        await session.delete(db_difficulty)
        await session.commit()
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.delete('/organizations/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(id: int, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.exec(select(Organization).where(Organization.id == id))
        db_organization = result.first()
        if not db_organization:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Organization not found')

        await session.delete(db_organization)
        await session.commit()
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.delete('/grades/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_grade(id: int, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.exec(select(Grade).where(Grade.id == id))
        db_grade = result.first()
        if not db_grade:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Grade not found')

        await session.delete(db_grade)
        await session.commit()
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.delete('/courses/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(id: int, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.exec(select(Course).where(Course.id == id))
        db_course = result.first()
        if not db_course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')

        await session.delete(db_course)
        await session.commit()
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@core_router.delete('/subjects/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(id: int, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.exec(select(Subject).where(Subject.id == id))
        db_subject = result.first()
        if not db_subject:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Subject not found')

        await session.delete(db_subject)
        await session.commit()
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
