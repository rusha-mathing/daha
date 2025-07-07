from datetime import date
from typing import List, AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession
from sqlalchemy.sql.sqltypes import String
from sqlalchemy import Column, JSON

postgres_db_name = 'daha_db'
db_url = f'postgresql+asyncpg://daha_user:SWP2025@localhost/{postgres_db_name}'
engine = create_async_engine(db_url, echo=True)


# one to many I suppose
class CourseSubjectLink(SQLModel, table=True):
    course_id: int = Field(foreign_key='course.id', primary_key=True)
    subject_id: int = Field(foreign_key='subject.id', primary_key=True)


class CourseGradeLink(SQLModel, table=True):
    course_id: int = Field(foreign_key='course.id', primary_key=True)
    grade_id: int = Field(foreign_key='grade.id', primary_key=True)


# base models
class Subject(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    type: str = Field(unique=True, index=True)
    label: str
    icon: str = Field(sa_column=Column(String))
    color: str
    additional_description: List[str] = Field(default=[], sa_column=Column(JSON))

    courses: List['Course'] = Relationship(back_populates='subjects', link_model=CourseSubjectLink)


class Difficulty(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    type: str = Field(unique=True, index=True)
    label: str
    icon: str = Field(sa_column=Column(String))
    color: str

    courses: List['Course'] = Relationship(back_populates='difficulty')


class SubjectUpdate(SQLModel):
    type: Optional[str] = None
    label: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    additional_description: Optional[List[str]] = None


class Organization(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    name: str = Field(unique=True)
    courses: List['Course'] = Relationship(back_populates='organization')


class Grade(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    grade: int = Field(unique=True)

    courses: List['Course'] = Relationship(back_populates='grades', link_model=CourseGradeLink)


class Course(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: str
    description: str
    start_date: date = Field(index=True)
    end_date: date = Field(index=True)
    url: str
    image_url: str
    organization_id: int = Field(foreign_key='organization.id', index=True)
    difficulty_id: int = Field(foreign_key='difficulty.id', index=True)

    organization: Organization = Relationship(back_populates='courses')
    difficulty: Difficulty = Relationship(back_populates='courses')
    subjects: List['Subject'] = Relationship(back_populates='courses', link_model=CourseSubjectLink)
    grades: List['Grade'] = Relationship(back_populates='courses', link_model=CourseGradeLink)


async def create_db_and_models():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SQLModelAsyncSession(bind=engine, expire_on_commit=False) as session:
        yield session


class DifficultyUpdate(SQLModel):
    type: Optional[str] = None
    label: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None


class CourseUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    organization: Optional[str] = None
    difficulty: Optional[str] = None
    subjects: Optional[List[str]] = None
    grades: Optional[List[int]] = None
