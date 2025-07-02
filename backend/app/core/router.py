from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.models import CourseResponse, SubjectResponse, OrganizationResponse, GradeResponse, DifficultyResponse
from app.models import get_session, Course, Subject, Organization, Grade, Difficulty

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
