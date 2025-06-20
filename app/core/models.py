from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

DEFAULT_LIMIT = 10


class SubjectResponse(BaseModel):
    id: int
    name: str


class OrganizationResponse(BaseModel):
    id: int
    name: str


class CourseResponse(BaseModel):
    id: int
    name: str
    url: str
    min_class: int
    max_class: int
    start: date
    end: date
    difficulty: int
    description: str
    organization: OrganizationResponse
    subject: SubjectResponse

    class Config:
        from_attributes = True


class CourseFilterParams(BaseModel):
    classes: Optional[list[int]] = Field(default=None, description='Classes')
    difficulties: Optional[list[int]] = Field(default=None, description='Difficulties')
    subjects: Optional[list[int]] = Field(default=None, description='Subjects id')
    organizations: Optional[list[int]] = Field(default=None, description='Organizations id')
    query: Optional[str] = Field(default=None, description='Name contain')
    offset: int = Field(0, ge=0, description='Offset')
    limit: int = Field(DEFAULT_LIMIT, ge=1, description='Limit')
