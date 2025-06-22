from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.core.models import CourseResponse, SubjectResponse, OrganizationResponse, GradeResponse, DifficultyResponse
from app.models import get_session, Course, Subject, Organization, Grade, Difficulty

core_router = APIRouter()


@core_router.get('/subjects/', response_model=List[SubjectResponse])
def get_subjects(session: Session = Depends(get_session)):
    subjects = session.exec(select(Subject)).all()
    return [
        SubjectResponse(
            id=subject.id,
            type=subject.type,
            label=subject.label,
            icon=subject.icon,
            color=subject.color,
            additional_description=subject.additional_description,
        )
        for subject in subjects
    ]


@core_router.get('/subjects/{id}', response_model=SubjectResponse)
def get_subject(id: int, session: Session = Depends(get_session)):
    subject = session.exec(select(Subject).where(Subject.id == id)).first()
    if not subject:
        raise HTTPException(status_code=404, detail='Subject not found')
    return SubjectResponse(
        id=subject.id,
        type=subject.type,
        label=subject.label,
        icon=subject.icon,
        color=subject.color,
        additional_description=subject.additional_description,
    )


@core_router.get('/difficulties/', response_model=List[DifficultyResponse])
def get_difficulties(session: Session = Depends(get_session)):
    difficulties = session.exec(select(Difficulty)).all()
    return [
        DifficultyResponse(
            id=difficulty.id, type=difficulty.type, label=difficulty.label, icon=difficulty.icon, color=difficulty.color
        )
        for difficulty in difficulties
    ]


@core_router.get('/difficulties/{id}', response_model=DifficultyResponse)
def get_difficulty(id: int, session: Session = Depends(get_session)):
    difficulty = session.exec(select(Difficulty).where(Difficulty.id == id)).first()
    if not difficulty:
        raise HTTPException(status_code=404, detail='Difficulty not found')
    return DifficultyResponse(
        id=difficulty.id, type=difficulty.type, label=difficulty.label, icon=difficulty.icon, color=difficulty.color
    )


@core_router.get('/organizations/', response_model=List[OrganizationResponse])
def get_organizations(session: Session = Depends(get_session)):
    organizations = session.exec(select(Organization)).all()
    return [OrganizationResponse(id=organization.id, name=organization.name) for organization in organizations]


@core_router.get('/organizations/{id}', response_model=OrganizationResponse)
def get_organization(id: int, session: Session = Depends(get_session)):
    organization = session.exec(select(Organization).where(Organization.id == id)).first()
    if not organization:
        raise HTTPException(status_code=404, detail='Organization not found')
    return OrganizationResponse(id=organization.id, name=organization.name)


@core_router.get('/grades/', response_model=List[GradeResponse])
def get_grades(session: Session = Depends(get_session)):
    grades = session.exec(select(Grade)).all()
    return [GradeResponse(id=grade.id, grade=grade.grade) for grade in grades]


@core_router.get('/grades/{id}', response_model=GradeResponse)
def get_grade(id: int, session: Session = Depends(get_session)):
    grade = session.exec(select(Grade).where(Grade.id == id)).first()
    if not grade:
        raise HTTPException(status_code=404, detail='Grade not found')
    return GradeResponse(id=grade.id, grade=grade.grade)


@core_router.get('/courses/', response_model=List[CourseResponse])
def get_courses(session: Session = Depends(get_session)):
    courses = session.exec(
        select(Course).options(
            selectinload(Course.subjects),
            selectinload(Course.grades),
            selectinload(Course.organization),
            selectinload(Course.difficulty),
        )
    ).all()
    return [
        CourseResponse(
            id=course.id,
            title=course.title,
            description=course.description,
            subject=[subject.type for subject in course.subjects],
            grades=[grade.grade for grade in course.grades],
            start=course.start_date,
            end=course.end_date,
            url=course.url,
            organization=course.organization.name,
            difficulty=course.difficulty.type,
        )
        for course in courses
    ]


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
    return CourseResponse(
        id=course.id,
        title=course.title,
        description=course.description,
        subject=[subject.type for subject in course.subjects],
        grades=[grade.grade for grade in course.grades],
        start=course.start_date,
        end=course.end_date,
        url=course.url,
        organization=course.organization.name,
        difficulty=course.difficulty.type,
    )
