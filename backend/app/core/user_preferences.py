from __future__ import annotations
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy import JSON, Column

class UserPreference(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True, index=True)
    
    # We can store lists of IDs for simplicity
    subject_ids: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
    grade_ids: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
    difficulty_ids: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
    organization_ids: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))

    user: "User" = Relationship(back_populates="preferences")

class UserPreferenceUpdate(BaseModel):
    subject_ids: Optional[List[int]] = None
    grade_ids: Optional[List[int]] = None
    difficulty_ids: Optional[List[int]] = None
    organization_ids: Optional[List[int]] = None

class UserPreferenceService:
    async def get_preferences(self, session: AsyncSession, user_id: int) -> Optional[UserPreference]:
        statement = select(UserPreference).where(UserPreference.user_id == user_id)
        result = await session.exec(statement)
        return result.one_or_none()

    async def update_preferences(self, session: AsyncSession, user_id: int, data: UserPreferenceUpdate) -> UserPreference:
        preferences = await self.get_preferences(session, user_id)
        if not preferences:
            preferences = UserPreference(user_id=user_id)
            session.add(preferences)
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(preferences, key, value)
            
        await session.commit()
        await session.refresh(preferences)
        return preferences

user_preference_service = UserPreferenceService() 