from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator, EmailStr
from pydantic_core.core_schema import ValidationInfo
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

# Base response models
class SubjectResponse(BaseModel):
    id: int
    type: str
    label: str
    icon: str
    color: str
    additional_description: List[str] = []

class DifficultyResponse(BaseModel):
    id: int
    type: str
    label: str
    icon: str
    color: str

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
    organization: OrganizationResponse
    difficulty: DifficultyResponse
    subjects: List[SubjectResponse]
    grades: List[GradeResponse]

# Create models with validation
class SubjectCreate(BaseModel):
    type: str = Field(..., min_length=1, max_length=50)
    label: str = Field(..., min_length=1, max_length=100)
    icon: str = Field(..., min_length=1, max_length=50)
    color: str = Field(..., pattern=r'^#[0-9A-Fa-f]{6}$')
    additional_description: List[str] = Field(default=[])

    @validator('type')
    def validate_type(cls, v):
        if not v.isalnum() and '_' not in v:
            raise ValueError('Type must be alphanumeric with underscores only')
        return v.lower()

class DifficultyCreate(BaseModel):
    type: str = Field(..., min_length=1, max_length=100)
    label: str = Field(..., min_length=1, max_length=100)
    icon: str = Field(..., min_length=1, max_length=50)
    color: str = Field(..., pattern=r'^#[0-9A-Fa-f]{6}$')

    @validator('type')
    def type_must_be_lowercase(cls, v: str) -> str:
        if not v.islower():
            raise ValueError('must be lowercase')
        return v

class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class GradeCreate(BaseModel):
    grade: int = Field(..., ge=1, le=12)

class CourseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10, max_length=1000)
    start_date: date
    end_date: date
    url: str = Field(..., pattern=r'^https?://.*')
    image_url: str = Field(..., pattern=r'^https?://.*')
    organization: str = Field(..., min_length=1, max_length=100)
    difficulty: str = Field(..., min_length=1, max_length=50)
    subjects: List[str] = Field(..., min_items=1)
    grades: List[int] = Field(..., min_items=1)

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v

    @validator('grades')
    def validate_grades(cls, v):
        for grade in v:
            if not 1 <= grade <= 12:
                raise ValueError('Grades must be between 1 and 12')
        return v

# Filter models
class CourseFilters(BaseModel):
    subject: Optional[str] = None
    difficulty: Optional[str] = None
    organization: Optional[str] = None
    grade: Optional[int] = Field(None, ge=1, le=12)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    search: Optional[str] = Field(None, max_length=100)

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v

# Response models
class CreateResponse(BaseModel):
    id: int
    message: str = "Created successfully"

class PaginatedResponse(BaseModel):
    items: List[CourseResponse]
    total: int
    page: int
    size: int
    pages: int
