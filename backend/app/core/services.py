from typing import List, TypeVar, Generic
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundError, DatabaseError, ValidationError
from app.models import Course, Subject, Difficulty, Organization, Grade, CourseUpdate

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
            raise DatabaseError(f'Failed to fetch {self.model.__name__} records: {str(e)}')

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
            raise DatabaseError(f'Failed to fetch {self.model.__name__}: {str(e)}')

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
            raise DatabaseError(f'Failed to create {self.model.__name__}: {str(e)}')

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
            raise DatabaseError(f'Failed to update {self.model.__name__}: {str(e)}')

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
            raise DatabaseError(f'Failed to delete {self.model.__name__}: {str(e)}')


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
            raise DatabaseError(f'Failed to fetch courses: {str(e)}')

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
                raise NotFoundError('Course', id)
            return course
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f'Failed to fetch course: {str(e)}')

    async def create_with_relations(
        self,
        session: AsyncSession,
        course_data: dict,
        difficulty_type: str,
        organization_name: str,
        subject_types: List[str],
        grade_values: List[int],
    ) -> Course:
        """Create a course with all its relationships"""
        try:
            # Get or create difficulty
            difficulty_result = await session.exec(select(Difficulty).where(Difficulty.type == difficulty_type))
            difficulty = difficulty_result.first()
            if not difficulty:
                raise NotFoundError('Difficulty', difficulty_type)

            # Get or create organization
            org_result = await session.exec(select(Organization).where(Organization.name == organization_name))
            organization = org_result.first()
            if not organization:
                organization = Organization(name=organization_name)
                session.add(organization)
                await session.commit()
                await session.refresh(organization)

            # Get subjects
            subjects_result = await session.exec(select(Subject).where(Subject.type.in_(subject_types)))
            subjects = subjects_result.all()
            if len(subjects) != len(subject_types):
                found_types = [s.type for s in subjects]
                missing = [s for s in subject_types if s not in found_types]
                raise NotFoundError(f'Subjects {missing}', 0)

            # Get or create grades
            grades = []
            for grade_value in grade_values:
                grade_result = await session.exec(select(Grade).where(Grade.grade == grade_value))
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
            raise DatabaseError(f'Failed to create course: {str(e)}')

    async def update_with_relations(self, session: AsyncSession, id: int, course_update: CourseUpdate) -> Course:
        """Update a course with all its relationships"""
        try:
            # Get course with relations
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
            db_course = result.first()
            if not db_course:
                raise NotFoundError('Course', id)

            # Update basic fields
            if course_update.title is not None:
                db_course.title = course_update.title
            if course_update.description is not None:
                db_course.description = course_update.description
            if course_update.start_date is not None:
                db_course.start_date = course_update.start_date
            if course_update.end_date is not None:
                db_course.end_date = course_update.end_date
            if course_update.url is not None:
                db_course.url = course_update.url
            if course_update.image_url is not None:
                db_course.image_url = course_update.image_url

            # Update difficulty
            if course_update.difficulty is not None:
                difficulty_result = await session.exec(
                    select(Difficulty).where(Difficulty.type == course_update.difficulty)
                )
                db_difficulty = difficulty_result.first()
                if not db_difficulty:
                    raise ValidationError('Difficulty not found')
                db_course.difficulty = db_difficulty

            # Update subjects
            if course_update.subjects is not None:
                if isinstance(course_update.subjects, str):
                    subject_result = await session.exec(select(Subject).where(Subject.type == course_update.subjects))
                    db_subject = subject_result.first()
                    if not db_subject:
                        raise ValidationError(f'Subject "{course_update.subjects}" not found')
                    db_course.subjects = [db_subject]
                elif isinstance(course_update.subjects, list):
                    subject_result = await session.exec(select(Subject).where(Subject.type.in_(course_update.subjects)))
                    db_subjects = subject_result.all()

                    if len(db_subjects) != len(course_update.subjects):
                        found_types = [s.type for s in db_subjects]
                        missing_subjects = [s for s in course_update.subjects if s not in found_types]
                        raise ValidationError(f'Subjects not found: {missing_subjects}')

                    db_course.subjects = db_subjects
                else:
                    raise ValidationError('Invalid subjects format. Must be a string or a list of strings.')

            # Update organization
            if course_update.organization is not None:
                org_result = await session.exec(
                    select(Organization).where(Organization.name == course_update.organization)
                )
                db_organization = org_result.first()
                if not db_organization:
                    db_organization = Organization(name=course_update.organization)
                    session.add(db_organization)
                    await session.commit()
                    await session.refresh(db_organization)
                db_course.organization = db_organization

            # Update grades
            if course_update.grades is not None:
                db_grades = []
                for grade_value in course_update.grades:
                    grade_result = await session.exec(select(Grade).where(Grade.grade == grade_value))
                    db_grade = grade_result.first()
                    if not db_grade:
                        db_grade = Grade(grade=grade_value)
                        session.add(db_grade)
                        await session.commit()
                        await session.refresh(db_grade)
                    db_grades.append(db_grade)

                db_course.grades.clear()
                db_course.grades.extend(db_grades)

            session.add(db_course)
            await session.commit()

            # Return updated course with relations
            return await self.get_by_id_with_relations(session, id)

        except (NotFoundError, DatabaseError):
            await session.rollback()
            raise
        except ValidationError:
            await session.rollback()
            raise
        except Exception as e:
            await session.rollback()
            raise DatabaseError(f'Failed to update course: {str(e)}')


# Service instances
subject_service = BaseService(Subject)
difficulty_service = BaseService(Difficulty)
organization_service = BaseService(Organization)
grade_service = BaseService(Grade)
course_service = CourseService()
