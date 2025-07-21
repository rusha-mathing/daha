from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from pydantic import BaseModel

from .models import UserCreate, UserLogin, UserResponse, TokenResponse, PasswordChange, UserUpdate
from .services import auth_service
from app.dependencies import get_session
from .models import User, UserRole
from .linking import linking_service
from app.core.user_preferences import user_preference_service, UserPreferenceUpdate, UserPreference

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LinkTelegramPayload(BaseModel):
    token: str
    telegram_id: int

@router.post("/generate-link-token", response_model=dict)
async def generate_link_token(
    current_user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Generate a short-lived token for linking a Telegram account."""
    token = await linking_service.generate_token(session, current_user.id)
    return {"link_token": token, "expires_in": 600}

@router.post("/link-telegram", response_model=UserResponse)
async def link_telegram_account(
    payload: LinkTelegramPayload,
    session: AsyncSession = Depends(get_session),
):
    """Link a Telegram account using a token."""
    user = await linking_service.link_account(session, payload.token, payload.telegram_id)
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        telegram_id=user.telegram_id,
        created_at=user.created_at,
        last_login=user.last_login,
    )

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    """Register a new user"""
    try:
        user = await auth_service.create_user(session, user_data)
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            telegram_id=user.telegram_id,
            created_at=user.created_at,
            last_login=user.last_login
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

@router.post("/login", response_model=TokenResponse)
async def login(
    user_data: UserLogin,
    session: AsyncSession = Depends(get_session),
):
    """Login user and get access token"""
    try:
        result = await auth_service.login_user(session, user_data)
        return TokenResponse(
            access_token=result["access_token"],
            token_type=result["token_type"],
            expires_in=result["expires_in"],
            user=UserResponse(**result["user"])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: User = Depends(auth_service.get_current_user)
):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        telegram_id=current_user.telegram_id,
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Update current user information"""
    try:
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(current_user, field, value)
        
        await session.commit()
        await session.refresh(current_user)
        
        return UserResponse(
            id=current_user.id,
            email=current_user.email,
            username=current_user.username,
            full_name=current_user.full_name,
            role=current_user.role,
            is_active=current_user.is_active,
            telegram_id=current_user.telegram_id,
            created_at=current_user.created_at,
            last_login=current_user.last_login
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )

@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    password_change: PasswordChange,
    current_user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Change user password"""
    try:
        if not auth_service.verify_password(password_change.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        current_user.hashed_password = auth_service.get_password_hash(password_change.new_password)
        await session.commit()
        
        return {"message": "Password changed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change password: {str(e)}"
        )

@router.post("/generate-telegram-token", status_code=status.HTTP_200_OK)
async def generate_telegram_token(
    current_user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Generate a token to link a Telegram account."""
    link_token = await linking_service.create_link_token(session, current_user.id)
    return {"token": link_token.token, "expires_at": link_token.expires_at}

@router.get("/me/preferences", response_model=UserPreference)
async def get_my_preferences(
    current_user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get current user's preferences."""
    preferences = await user_preference_service.get_preferences(session, current_user.id)
    if not preferences:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return preferences

@router.put("/me/preferences", response_model=UserPreference)
async def update_my_preferences(
    data: UserPreferenceUpdate,
    current_user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Update current user's preferences."""
    return await user_preference_service.update_preferences(session, current_user.id, data)

# Admin endpoints
@router.get("/users", response_model=List[UserResponse])
async def get_users(
    current_user: User = Depends(auth_service.require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(get_session),
):
    """Get all users (admin only)"""
    from sqlmodel import select
    result = await session.exec(select(User))
    users = result.all()
    return [
        UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            telegram_id=user.telegram_id,
            created_at=user.created_at,
            last_login=user.last_login
        )
        for user in users
    ]

@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    role: UserRole,
    current_user: User = Depends(auth_service.require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(get_session),
):
    """Update user role (admin only)"""
    from sqlmodel import select
    user = await session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.role = role
    await session.commit()
    return {"message": f"User role updated to {role}"}

@router.put("/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    current_user: User = Depends(auth_service.require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(get_session),
):
    """Toggle user active status (admin only)"""
    from sqlmodel import select
    user = await session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = not user.is_active
    await session.commit()
    return {"message": f"User active status changed to {user.is_active}"} 