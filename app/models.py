from datetime import date
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel, Session, create_engine

sqlite_file_name = 'db.sqlite3'
sqlite_url = f'sqlite:///{sqlite_file_name}'
engine = create_engine(sqlite_url, echo=True)


class PreferenceSubjectLink(SQLModel, table=True):
    preference_id: Optional[int] = Field(default=None, foreign_key='preference.id', primary_key=True)
    subject_id: Optional[int] = Field(default=None, foreign_key='subject.id', primary_key=True)


class Subject(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(index=True)

    courses: List['Course'] = Relationship(back_populates='subject')
    preferences: List['Preference'] = Relationship(back_populates='subjects', link_model=PreferenceSubjectLink)


class Organization(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(index=True)

    courses: List['Course'] = Relationship(back_populates='organization')


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    username: str = Field(unique=True)
    preference_id: Optional[int] = Field(default=None, foreign_key='preference.id')

    preference: Optional['Preference'] = Relationship(back_populates='user')


class Preference(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    preferred_class: int = Field(default=7, ge=1, le=11, description='Preferred school class (1-11)')
    preferred_difficulty: int = Field(default=3, ge=1, le=5, description='Preferred difficulty level (1-5)')

    user: Optional['User'] = Relationship(back_populates='preference')
    subjects: List['Subject'] = Relationship(back_populates='preferences', link_model=PreferenceSubjectLink)


class Course(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    url: str
    organization_id: int = Field(foreign_key='organization.id')
    subject_id: int = Field(foreign_key='subject.id')  # Fixed: was organization.id
    min_class: int = Field(ge=1, le=11)
    max_class: int = Field(ge=1, le=11)
    start: date
    end: date
    difficulty: int = Field(default=1, ge=1, le=3, description='Course difficulty level (1-3)')
    description: str

    organization: Organization = Relationship(back_populates='courses')
    subject: Subject = Relationship(back_populates='courses')


def create_db_and_models():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def create_fixtures():
    with Session(engine) as session:
        # Create subjects
        math = Subject(name='Mathematics')
        physics = Subject(name='Physics')
        programming = Subject(name='Programming')
        session.add_all([math, physics, programming])
        session.commit()

        # Create organizations
        org1 = Organization(name='Coding Academy')
        org2 = Organization(name='Science School')
        session.add_all([org1, org2])
        session.commit()

        # Create courses
        courses = [
            Course(
                name='Algebra Basics',
                url='https://example.com/algebra',
                organization_id=org1.id,
                subject_id=math.id,
                min_class=5,
                max_class=8,
                start=date(2023, 9, 1),
                end=date(2024, 1, 15),
                difficulty=2,
                description='Introduction to algebra',
            ),
            Course(
                name='Python Fundamentals',
                url='https://example.com/python',
                organization_id=org1.id,
                subject_id=programming.id,
                min_class=7,
                max_class=11,
                start=date(2023, 10, 1),
                end=date(2024, 3, 1),
                difficulty=3,
                description='Learn Python programming',
            ),
            Course(
                name='Physics for Beginners',
                url='https://example.com/physics',
                organization_id=org2.id,
                subject_id=physics.id,
                min_class=6,
                max_class=9,
                start=date(2023, 9, 15),
                end=date(2024, 2, 28),
                difficulty=3,
                description='Basic physics concepts',
            ),
        ]
        session.add_all(courses)
        session.commit()

        # Create preferences
        pref1 = Preference(preferred_class=8, preferred_difficulty=3, subjects=[math, programming])

        pref2 = Preference(preferred_class=10, preferred_difficulty=4, subjects=[physics, programming])
        session.add_all([pref1, pref2])
        session.commit()

        # Create users
        users = [
            User(username='student1', preference=pref1),
            User(username='student2', preference=pref2),
            User(username='student3'),  # No preferences
        ]
        session.add_all(users)
        session.commit()

        print('Successfully created fixtures!')
