from typing import List, Optional, TypeVar, Generic
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundError, DatabaseError
from app.models import Course, Subject, Difficulty, Organization, Grade

T = TypeVar('T', bound=SQLModel)


class BaseService(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model

    async def get_all(self, session: AsyncSession) -> List[T]:
        """Get all records of the model"""
        try:
            result = await session.exec(select(self.model))
            return result.all()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch {self.model.__name__} records: {str(e)}")

    async def get_by_id(self, session: AsyncSession, id: int) -> T:
        """Get a record by ID"""
        try:
            result = await session.exec(select(self.model).where(self.model.id == id))
            record = result.first()
            if not record:
                raise NotFoundError(self.model.__name__, id)
            return record
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to fetch {self.model.__name__}: {str(e)}")

    async def create(self, session: AsyncSession, data: dict) -> T:
        """Create a new record"""
        try:
            record = self.model(**data)
            session.add(record)
            await session.commit()
            await session.refresh(record)
            return record
        except Exception as e:
            await session.rollback()
            raise DatabaseError(f"Failed to create {self.model.__name__}: {str(e)}")

    async def update(self, session: AsyncSession, id: int, data: dict) -> T:
        """Update a record"""
        try:
            record = await self.get_by_id(session, id)
            for key, value in data.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            session.add(record)
            await session.commit()
            await session.refresh(record)
            return record
        except NotFoundError:
            raise
        except Exception as e:
            await session.rollback()
            raise DatabaseError(f"Failed to update {self.model.__name__}: {str(e)}")

    async def delete(self, session: AsyncSession, id: int) -> None:
        """Delete a record"""
        try:
            record = await self.get_by_id(session, id)
            await session.delete(record)
            await session.commit()
        except NotFoundError:
            raise
        except Exception as e:
            await session.rollback()
            raise DatabaseError(f"Failed to delete {self.model.__name__}: {str(e)}")


class CourseService(BaseService[Course]):
    def __init__(self):
        super().__init__(Course)

    async def get_all_with_relations(self, session: AsyncSession) -> List[Course]:
        """Get all courses with their relationships loaded"""
        try:
            result = await session.exec(
                select(Course).options(
                    selectinload(Course.subjects),
                    selectinload(Course.grades),
                    selectinload(Course.organization),
                    selectinload(Course.difficulty),
                )
            )
            return result.all()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch courses: {str(e)}")

    async def get_by_id_with_relations(self, session: AsyncSession, id: int) -> Course:
        """Get a course by ID with relationships loaded"""
        try:
            result = await session.exec(
                select(Course)
                .where(Course.id == id)
                .options(
                    selectinload(Course.subjects),
                    selectinload(Course.grades),
                    selectinload(Course.organization),
                    selectinload(Course.difficulty),
                )
            )
            course = result.first()
            if not course:
                raise NotFoundError("Course", id)
            return course
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to fetch course: {str(e)}")

    async def create_with_relations(
        self, 
        session: AsyncSession, 
        course_data: dict,
        difficulty_type: str,
        organization_name: str,
        subject_types: List[str],
        grade_values: List[int]
    ) -> Course:
        """Create a course with all its relationships"""
        try:
            # Get or create difficulty
            difficulty_result = await session.exec(
                select(Difficulty).where(Difficulty.type == difficulty_type)
            )
            difficulty = difficulty_result.first()
            if not difficulty:
                raise NotFoundError("Difficulty", difficulty_type)

            # Get or create organization
            org_result = await session.exec(
                select(Organization).where(Organization.name == organization_name)
            )
            organization = org_result.first()
            if not organization:
                organization = Organization(name=organization_name)
                session.add(organization)
                await session.commit()
                await session.refresh(organization)

            # Get subjects
            subjects_result = await session.exec(
                select(Subject).where(Subject.type.in_(subject_types))
            )
            subjects = subjects_result.all()
            if len(subjects) != len(subject_types):
                found_types = [s.type for s in subjects]
                missing = [s for s in subject_types if s not in found_types]
                raise NotFoundError(f"Subjects {missing}", 0)

            # Get or create grades
            grades = []
            for grade_value in grade_values:
                grade_result = await session.exec(
                    select(Grade).where(Grade.grade == grade_value)
                )
                grade = grade_result.first()
                if not grade:
                    grade = Grade(grade=grade_value)
                    session.add(grade)
                    await session.commit()
                    await session.refresh(grade)
                grades.append(grade)

            # Create course
            course = Course(
                **course_data,
                organization=organization,
                difficulty=difficulty,
            )
            session.add(course)
            await session.commit()
            await session.refresh(course)

            # Add relationships
            from app.models import CourseSubjectLink, CourseGradeLink
            for subject in subjects:
                link = CourseSubjectLink(course_id=course.id, subject_id=subject.id)
                session.add(link)

            for grade in grades:
                link = CourseGradeLink(course_id=course.id, grade_id=grade.id)
                session.add(link)

            await session.commit()
            return await self.get_by_id_with_relations(session, course.id)

        except NotFoundError:
            await session.rollback()
            raise
        except Exception as e:
            await session.rollback()
            raise DatabaseError(f"Failed to create course: {str(e)}")


# Service instances
subject_service = BaseService(Subject)
difficulty_service = BaseService(Difficulty)
organization_service = BaseService(Organization)
grade_service = BaseService(Grade)
course_service = CourseService() 