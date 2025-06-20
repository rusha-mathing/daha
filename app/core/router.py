from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, and_, or_
from sqlalchemy.orm import selectinload

from app.models import get_session, Course, Subject, Organization
from app.core.models import CourseResponse, SubjectResponse, OrganizationResponse, CourseFilterParams


core_router = APIRouter()


@core_router.get('/courses/', response_model=List[CourseResponse])
async def get_courses(course_filter: Annotated[CourseFilterParams, Query()], db: Session = Depends(get_session)):
    query = select(Course).options(selectinload(Course.organization)).options(selectinload(Course.subject))

    conditions = []
    if course_filter.classes:
        conditions.append(
            or_(
                *(
                    and_(Course.min_class <= class_level, Course.max_class >= class_level)
                    for class_level in course_filter.classes
                )
            )
        )
    if course_filter.difficulties:
        conditions.append(Course.difficulty.in_(course_filter.difficulties))
    if course_filter.query:
        conditions.append(Course.name.contains(course_filter.query))
    if course_filter.organizations:
        conditions.append(Course.organization_id.in_(course_filter.organizations))
    if course_filter.subjects:
        conditions.append(Course.subject_id.in_(course_filter.subjects))
    if conditions:
        query = query.where(and_(*conditions))
    courses = db.exec(query.offset(course_filter.offset).limit(course_filter.limit)).all()

    return courses


@core_router.get('/courses/{course_id}/', response_model=CourseResponse)
async def get_course(course_id: int, db: Session = Depends(get_session)):
    course = db.exec(
        select(Course)
        .where(Course.id == course_id)
        .options(selectinload(Course.organization))
        .options(selectinload(Course.subject))
    ).one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail='Course not found')

    return course


@core_router.get('/subjects/', response_model=List[SubjectResponse])
async def get_subjects(db: Session = Depends(get_session)):
    subjects = db.exec(select(Subject)).all()
    return subjects


@core_router.get('/subjects/{subject_id}/', response_model=SubjectResponse)
async def get_subject(subject_id: int, db: Session = Depends(get_session)):
    subject = db.exec(select(Subject).where(Subject.id == subject_id)).one_or_none()
    if not subject:
        raise HTTPException(status_code=404, detail='Subject not found')
    return subject


@core_router.get('/organizations/', response_model=List[OrganizationResponse])
async def get_organizations(db: Session = Depends(get_session)):
    organizations = db.exec(select(Organization)).all()
    return organizations


@core_router.get('/organizations/{organization_id}/', response_model=OrganizationResponse)
async def get_organization(organization_id: int, db: Session = Depends(get_session)):
    organization = db.exec(select(Organization).where(Organization.id == organization_id)).one_or_none()
    if not organization:
        raise HTTPException(status_code=404, detail='Organization not found')
    return organization
