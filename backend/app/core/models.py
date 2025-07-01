from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict, field_validator

from app.models import Grade, Difficulty, Subject, Organization


class FilterResponse(BaseModel):
    id: int
    type: str
    label: str
    icon: str
    color: str


class SubjectResponse(FilterResponse):
    additional_description: List[str]


class DifficultyResponse(FilterResponse):
    pass


class OrganizationResponse(BaseModel):
    id: int
    name: str


class GradeResponse(BaseModel):
    id: int
    grade: int


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    start_date: date
    end_date: date
    url: str
    image_url: str
    model_config = ConfigDict(from_attributes=True)  # pydantic v2

    grades: List[int]

    @field_validator('grades', mode='before')
    @classmethod
    def serialize_grades(cls, grades: List[Grade]) -> List[int]:
        return [int(i.grade) for i in grades]

    difficulty: str

    @field_validator('difficulty', mode='before')
    @classmethod
    def serialize_difficulty(cls, difficulty: Difficulty) -> str:
        return difficulty.type

    subjects: List[str]

    @field_validator('subjects', mode='before')
    @classmethod
    def serialize_subjects(cls, subjects: List[Subject]) -> List[str]:
        return [str(i.type) for i in subjects]

    organization: str

    @field_validator('organization', mode='before')
    @classmethod
    def serialize_organization(cls, organization: Organization) -> str:
        return organization.name


class SubjectCreate(BaseModel):
    type: str
    label: str
    icon: str
    color: str
    additional_description: List[str]


class DifficultyCreate(BaseModel):
    type: str
    label: str
    icon: str
    color: str


class OrganizationCreate(BaseModel):
    name: str


class GradeCreate(BaseModel):
    grade: int


class CourseCreate(BaseModel):
    title: str
    description: str
    start_date: date
    end_date: date
    url: str
    image_url: str
    grades: List[int]
    difficulty: str
    subjects: List[str]
    organization: str
