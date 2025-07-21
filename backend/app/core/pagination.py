from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel, Field
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.config import settings

T = TypeVar('T', bound=SQLModel)

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Page size")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(cls, items: List[T], total: int, page: int, size: int) -> "PaginatedResponse[T]":
        pages = (total + size - 1) // size
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1
        )

async def paginate_query(
    session: AsyncSession,
    query,
    pagination: PaginationParams
) -> PaginatedResponse:
    """Apply pagination to a query"""
    # Get total count
    count_query = select(query.subquery().count())
    total_result = await session.exec(count_query)
    total = total_result.first()

    # Apply pagination
    offset = (pagination.page - 1) * pagination.size
    paginated_query = query.offset(offset).limit(pagination.size)
    
    # Execute query
    result = await session.exec(paginated_query)
    items = result.all()

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        size=pagination.size
    ) 