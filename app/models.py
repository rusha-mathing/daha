from datetime import date
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel, create_engine


sqlite_file_name = 'db.sqlite3'
sqlite_url = f'sqlite:///{sqlite_file_name}'
engine = create_engine(sqlite_url, echo=True)


class PreferenceSubjectLink(SQLModel, table=True):
    preference_id: Optional[int] = Field(default=None, foreign_key='preference.id', primary_key=True)
    subject_id: Optional[int] = Field(default=None, foreign_key='subject.id', primary_key=True)


class Subject(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    courses: list['Course'] = Relationship(back_populates='subject')


class Organization(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    courses: list['Course'] = Relationship(back_populates='organization')


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    preference_id: Optional[int] = Field(default=None, foreign_key='preference.id')
    preference: Optional['Preference'] = Relationship(back_populates='user')


class Preference(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    prefered_class: int
    prefered_difficult: int

    user: User = Relationship(back_populates='preference')
    subjects: list[Subject] = Relationship(back_populates='preferences', link_model=PreferenceSubjectLink)


class Course(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    url: str
    organization_id: int = Field(foreign_key='organization.id')
    subject_id: int = Field(foreign_key='organization.id')
    min_class: int
    max_class: int
    start: date
    end: date

    difficult: int

    description: str

    organization: Organization = Relationship(back_populates='courses')
    subject: Subject = Relationship(back_populates='courses')


def create_db_and_models():
    SQLModel.metadata.create_all(engine)
