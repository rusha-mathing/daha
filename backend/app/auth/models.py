from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    email: EmailStr = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)
    telegram_id: Optional[int] = Field(default=None, unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    sessions: List["UserSession"] = Relationship(back_populates="user")
    preferences: Optional["UserPreference"] = Relationship(back_populates="user")


class UserSession(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="user.id")
    token_hash: str = Field(unique=True, index=True)
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    user: User = Relationship(back_populates="sessions")


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: UserRole
    is_active: bool
    telegram_id: Optional[int] = None
    created_at: datetime
    last_login: Optional[datetime] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
