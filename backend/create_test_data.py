import asyncio
import logging
from typing import Dict, Any, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import get_password_hash
from app.models import (
    User, UserRole, Organization, Grade, Subject, Difficulty, Course,
    CourseSubject, CourseGrade, CourseOrganization,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_test_data(db: AsyncSession) -> None:
    logger.info("Creating test data...")

    # Create users
    users_data = [
        {"email": "test.user@example.com", "password": "password123", "role": "user", "full_name": "Test User"},
        {"email": "test.admin@example.com", "password": "password123", "role": "admin", "full_name": "Test Admin"},
    ]
    users: Dict[str, User] = {}
    for user_data in users_data:
        hashed_password = get_password_hash(user_data["password"])
        user = User(
            email=user_data["email"],
            hashed_password=hashed_password,
            full_name=user_data["full_name"],
            role=UserRole[user_data["role"]],
            is_active=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        users[user_data["email"]] = user
        logger.info(f"Created user: {user.email}")

    # Create organizations
    organizations_data = [
        {"name": "Школа 'Интеллект'", "description": "Образовательное учреждение с углубленным изучением предметов."},
        {"name": "Лицей 'Перспектива'", "description": "Современный лицей с фокусом на IT и инженерию."},
        {"name": "Гимназия 'Гармония'", "description": "Гимназия с гуманитарным уклоном."},
    ]
    organizations: Dict[str, Organization] = {}
    for org_data in organizations_data:
        organization = Organization(**org_data)
        db.add(organization)
        await db.commit()
        await db.refresh(organization)
        organizations[org_data["name"]] = organization
        logger.info(f"Created organization: {organization.name}")

    # Create grades
    grades_data = [
        {"name": "9 класс", "level": 9},
        {"name": "10 класс", "level": 10},
        {"name": "11 класс", "level": 11},
    ]
    grades: Dict[str, Grade] = {}
    for grade_data in grades_data:
        grade = Grade(**grade_data)
        db.add(grade)
        await db.commit()
        await db.refresh(grade)
        grades[grade_data["name"]] = grade
        logger.info(f"Created grade: {grade.name}")

    # Create subjects
    subjects_data = [
        {"name": "Математика", "description": "Царица наук."},
        {"name": "Физика", "description": "Наука о природе."},
        {"name": "Химия", "description": "Наука о веществах."},
        {"name": "Биология", "description": "Наука о живых организмах."},
        {"name": "История", "description": "Наука о прошлом."},
    ]
    subjects: Dict[str, Subject] = {}
    for subject_data in subjects_data:
        subject = Subject(**subject_data)
        db.add(subject)
        await db.commit()
        await db.refresh(subject)
        subjects[subject_data["name"]] = subject
        logger.info(f"Created subject: {subject.name}")

    # Create difficulties
    difficulties_data = [
        {"name": "Легкий", "description": "Для начинающих."},
        {"name": "Средний", "description": "Для продвинутых."},
        {"name": "Сложный", "description": "Для экспертов."},
    ]
    difficulties: Dict[str, Difficulty] = {}
    for diff_data in difficulties_data:
        difficulty = Difficulty(**diff_data)
        db.add(difficulty)
        await db.commit()
        await db.refresh(difficulty)
        difficulties[diff_data["name"]] = difficulty
        logger.info(f"Created difficulty: {difficulty.name}")

    # Create courses
    courses_data = [
        {
            "name": "Алгебра 9 класс", "description": "Полный курс алгебры для 9 класса.",
            "difficulty": "Средний", "subjects": ["Математика"], "grades": ["9 класс"], "organizations": ["Школа 'Интеллект'"]
        },
        {
            "name": "Механика для начинающих", "description": "Введение в классическую механику.",
            "difficulty": "Легкий", "subjects": ["Физика"], "grades": ["10 класс"], "organizations": ["Лицей 'Перспектива'"]
        },
        {
            "name": "Органическая химия", "description": "Глубокое погружение в органическую химию.",
            "difficulty": "Сложный", "subjects": ["Химия"], "grades": ["11 класс"], "organizations": ["Гимназия 'Гармония'"]
        },
    ]

    for course_data in courses_data:
        difficulty = difficulties[course_data["difficulty"]]
        course = Course(
            name=course_data["name"],
            description=course_data["description"],
            difficulty_id=difficulty.id,
            created_by_id=users["test.admin@example.com"].id,
        )
        db.add(course)
        await db.commit()
        await db.refresh(course)

        for subject_name in course_data["subjects"]:
            subject = subjects[subject_name]
            course_subject = CourseSubject(course_id=course.id, subject_id=subject.id)
            db.add(course_subject)

        for grade_name in course_data["grades"]:
            grade = grades[grade_name]
            course_grade = CourseGrade(course_id=course.id, grade_id=grade.id)
            db.add(course_grade)

        for org_name in course_data["organizations"]:
            organization = organizations[org_name]
            course_organization = CourseOrganization(course_id=course.id, organization_id=organization.id)
            db.add(course_organization)

        await db.commit()
        logger.info(f"Created course: {course.name}")

    logger.info("Test data created successfully.")


async def clear_test_data(db: AsyncSession) -> None:
    logger.info("Clearing test data...")

    # Clear join tables first to avoid foreign key violations
    await db.execute(CourseSubject.__table__.delete())
    await db.execute(CourseGrade.__table__.delete())
    await db.execute(CourseOrganization.__table__.delete())

    # Clear main tables
    await db.execute(Course.__table__.delete())
    await db.execute(User.__table__.delete())
    await db.execute(Organization.__table__.delete())
    await db.execute(Grade.__table__.delete())
    await db.execute(Subject.__table__.delete())
    await db.execute(Difficulty.__table__.delete())

    await db.commit()
    logger.info("Test data cleared successfully.")


async def main():
    from app.core.db import get_session

    db: AsyncSession = await anext(get_session())
    try:
        if settings.RECREATE_DB_ON_STARTUP:
            await clear_test_data(db)
            await create_test_data(db)
        else:
            logger.info("Skipping test data creation as RECREATE_DB_ON_STARTUP is False.")
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
