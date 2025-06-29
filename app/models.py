from datetime import date
from typing import List

from sqlmodel import Field, Relationship, SQLModel, Session, create_engine
from sqlalchemy.sql.sqltypes import String
from sqlalchemy import Column, JSON

sqlite_file_name = 'db.sqlite3'
sqlite_url = f'sqlite:///{sqlite_file_name}'
engine = create_engine(sqlite_url, echo=True)


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


def create_db_and_models():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
