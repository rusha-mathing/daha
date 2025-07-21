from datetime import datetime, timedelta
from typing import Optional
import secrets
import logging

from sqlmodel import Field, SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.auth.models import User

logger = logging.getLogger(__name__)

class LinkToken(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True, unique=True)
    token: str = Field(unique=True, index=True)
    expires_at: datetime

class LinkingService:
    async def generate_token(self, session: AsyncSession, user_id: int) -> str:
        # Invalidate old tokens for the user
        existing_token = await session.exec(
            select(LinkToken).where(LinkToken.user_id == user_id)
        ).first()
        if existing_token:
            await session.delete(existing_token)

        token = secrets.token_hex(16)
        expires_at = datetime.utcnow() + timedelta(minutes=10) # Token is valid for 10 minutes
        link_token = LinkToken(user_id=user_id, token=token, expires_at=expires_at)
        
        session.add(link_token)
        await session.commit()
        await session.refresh(link_token)
        
        logger.info(f"Generated link token for user {user_id}")
        return token

    async def link_account(self, session: AsyncSession, token: str, telegram_id: int) -> User:
        # Check if telegram_id is already linked
        existing_user_link = await session.exec(
            select(User).where(User.telegram_id == telegram_id)
        ).first()
        if existing_user_link:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This Telegram account is already linked to another user."
            )

        statement = select(LinkToken).where(LinkToken.token == token)
        link_token = (await session.exec(statement)).first()

        if not link_token or link_token.expires_at < datetime.utcnow():
            if link_token:
                await session.delete(link_token)
                await session.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Link token is invalid or has expired."
            )

        user = await session.get(User, link_token.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if user.telegram_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This user account is already linked to a Telegram account."
            )

        user.telegram_id = telegram_id
        await session.delete(link_token) # Token is single-use
        await session.commit()
        await session.refresh(user)

        logger.info(f"Successfully linked user {user.id} with Telegram account {telegram_id}")
        return user

linking_service = LinkingService() 