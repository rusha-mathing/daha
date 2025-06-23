from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.core.models import CourseResponse, SubjectResponse, OrganizationResponse, GradeResponse, DifficultyResponse
from app.models import get_session, Course, Subject, Organization, Grade, Difficulty

core_router = APIRouter()


@core_router.get('/subjects/', response_model=List[SubjectResponse])
def get_subjects(session: Session = Depends(get_session)):
    return session.exec(select(Subject)).all()


@core_router.get('/subjects/{id}', response_model=SubjectResponse)
def get_subject(id: int, session: Session = Depends(get_session)):
    subject = session.exec(select(Subject).where(Subject.id == id)).first()
    if not subject:
        raise HTTPException(status_code=404, detail='Subject not found')
    return subject


@core_router.get('/difficulties/', response_model=List[DifficultyResponse])
def get_difficulties(session: Session = Depends(get_session)):
    difficulties = session.exec(select(Difficulty)).all()
    return difficulties


@core_router.get('/difficulties/{id}', response_model=DifficultyResponse)
def get_difficulty(id: int, session: Session = Depends(get_session)):
    difficulty = session.exec(select(Difficulty).where(Difficulty.id == id)).first()
    if not difficulty:
        raise HTTPException(status_code=404, detail='Difficulty not found')
    return difficulty


@core_router.get('/organizations/', response_model=List[OrganizationResponse])
def get_organizations(session: Session = Depends(get_session)):
    return session.exec(select(Organization)).all()


@core_router.get('/organizations/{id}', response_model=OrganizationResponse)
def get_organization(id: int, session: Session = Depends(get_session)):
    organization = session.exec(select(Organization).where(Organization.id == id)).first()
    if not organization:
        raise HTTPException(status_code=404, detail='Organization not found')
    return organization


@core_router.get('/grades/', response_model=List[GradeResponse])
def get_grades(session: Session = Depends(get_session)):
    return session.exec(select(Grade)).all()


@core_router.get('/grades/{id}', response_model=GradeResponse)
def get_grade(id: int, session: Session = Depends(get_session)):
    grade = session.exec(select(Grade).where(Grade.id == id)).first()
    if not grade:
        raise HTTPException(status_code=404, detail='Grade not found')
    return grade


@core_router.get('/courses/', response_model=List[CourseResponse])
def get_courses(session: Session = Depends(get_session)):
    return session.exec(
        select(Course).options(
            selectinload(Course.subjects),
            selectinload(Course.grades),
            selectinload(Course.organization),
            selectinload(Course.difficulty),
        )
    ).all()


@core_router.get('/courses/{id}', response_model=CourseResponse)
def get_course(id: int, session: Session = Depends(get_session)):
    course = session.exec(
        select(Course)
        .where(Course.id == id)
        .options(
            selectinload(Course.subjects),
            selectinload(Course.grades),
            selectinload(Course.organization),
            selectinload(Course.difficulty),
        )
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    return course
