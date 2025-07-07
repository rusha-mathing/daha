import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, select, and_

engine = create_async_engine("sqlite+aiosqlite:///./bot.db", echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    subjects = relationship("UserSubject", back_populates="user", cascade="all, delete")
    difficulties = relationship("UserDifficulty", back_populates="user", cascade="all, delete")


class UserSubject(Base):
    __tablename__ = "user_subjects"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject_type = Column(String)
    user = relationship("User", back_populates="subjects")
    __table_args__ = (UniqueConstraint("user_id", "subject_type"),)

class UserDifficulty(Base):
    __tablename__ = "user_difficulties"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    difficulty_type = Column(String)
    user = relationship("User", back_populates="difficulties")
    __table_args__ = (UniqueConstraint("user_id", "difficulty_type"),)

async def get_or_create_user(session, telegram_id):
    res = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = res.scalar_one_or_none()
    if not user:
        user = User(telegram_id=telegram_id)
        session.add(user)
        await session.flush()
    return user

async def invert_subject(telegram_id, subject_type):
    async with async_session() as session:
        user = await get_or_create_user(session, telegram_id)
        res = await session.execute(
            select(UserSubject).where(
                UserSubject.user_id == user.id,
                UserSubject.subject_type == subject_type
            )
        )
        existing = res.scalar_one_or_none()
        if not existing:
            session.add(UserSubject(user_id=user.id, subject_type=subject_type))
        else:
            await session.delete(existing)
        await session.commit()

async def invert_difficulty(telegram_id, difficulty_type):
    async with async_session() as session:
        user = await get_or_create_user(session, telegram_id)
        res = await session.execute(
            select(UserDifficulty).where(
                UserDifficulty.user_id == user.id,
                UserDifficulty.difficulty_type == difficulty_type
            )
        )
        existing = res.scalar_one_or_none()
        if not existing:
            session.add(UserDifficulty(user_id=user.id, difficulty_type=difficulty_type))
        else:
            await session.delete(existing)
        await session.commit()

async def get_users_by_difficulty_and_subject(difficulty_type, subject_type):
    print(difficulty_type, subject_type)
    async with async_session() as session:
        stmt = (
            select(User).distinct()
            .join(UserDifficulty)
            .join(UserSubject)
            .where(
                and_(
                    UserDifficulty.difficulty_type == difficulty_type,
                    UserSubject.subject_type == subject_type,
                )
            )
        )
        result = await session.execute(stmt)
        return result.scalars().all()

async def get_subjects_by_telegram_id(telegram_id):
    async with async_session() as session:
        stmt = (
            select(UserSubject.subject_type)
            .join(User, User.id == UserSubject.user_id)
            .where(User.telegram_id == telegram_id)
        )
        result = await session.execute(stmt)
        return [row[0] for row in result.all()]

async def get_difficulties_by_telegram_id(telegram_id):
    async with async_session() as session:
        stmt = (
            select(UserDifficulty.difficulty_type)
            .join(User, User.id == UserDifficulty.user_id)
            .where(User.telegram_id == telegram_id)
        )
        result = await session.execute(stmt)
        return [row[0] for row in result.all()]

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())
