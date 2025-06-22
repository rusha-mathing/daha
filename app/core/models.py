from datetime import date
from typing import List

from pydantic import BaseModel

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
    subject: List[str]
    grades: List[int]
    start: date
    end: date
    url: str
    organization: str
    difficulty: str