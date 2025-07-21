import pytest
from datetime import date
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.services import course_service, subject_service, organization_service, grade_service, difficulty_service
from app.core.middleware import ErrorHandlingMiddleware
from app.core.exceptions import DatabaseError
from app.models import Course, Subject, Organization, Grade, Difficulty, CourseSubjectLink, CourseGradeLink
from fastapi import HTTPException, Request
from sqlalchemy.sql import select


class TestCourseService:
    """Test CourseService with real database"""

    @pytest.mark.asyncio
    async def test_get_courses_with_relations(self, session: AsyncSession):
        """Test getting courses with relations"""
        result = await course_service.get_all_with_relations(session)

        assert result is not None
        assert len(result) > 0
        assert all(isinstance(course, Course) for course in result)

    @pytest.mark.asyncio
    async def test_get_course_by_id_with_relations(self, session: AsyncSession):
        """Test getting a course by ID with relations"""
        # First get a course to test with
        courses = await course_service.get_all_with_relations(session)
        course_id = courses[0].id

        result = await course_service.get_by_id_with_relations(session, course_id)
        assert result is not None
        assert result.id == course_id
        assert result.title is not None

    @pytest.mark.asyncio
    async def test_create_course_with_relations(self, session: AsyncSession):
        """Test creating a new course with relations"""
        course_data = {
            'title': 'Test Course',
            'description': 'Test Description',
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 6, 1),
            'url': 'https://test.com',
            'image_url': 'https://test.com/image.jpg',
        }

        result = await course_service.create_with_relations(
            session,
            course_data,
            difficulty_type='beginner',
            organization_name='Test Academy',
            subject_types=['programming'],
            grade_values=[7, 8],
        )

        assert result is not None
        assert result.title == 'Test Course'
        assert result.description == 'Test Description'
        assert result.difficulty.type == 'beginner'
        assert result.organization.name == 'Test Academy'
        assert len(result.subjects) == 1
        assert len(result.grades) == 2

    @pytest.mark.asyncio
    async def test_update_course_with_relations(self, session: AsyncSession):
        """Test updating a course with relations"""
        from app.models import CourseUpdate

        # First get a course to update
        courses = await course_service.get_all_with_relations(session)
        course_id = courses[0].id

        update_data = CourseUpdate(title='Updated Course Title', description='Updated Description')

        result = await course_service.update_with_relations(session, course_id, update_data)
        assert result is not None
        assert result.title == 'Updated Course Title'
        assert result.description == 'Updated Description'


class TestSubjectService:
    """Test SubjectService with real database"""

    @pytest.mark.asyncio
    async def test_get_subjects(self, session: AsyncSession):
        """Test getting all subjects"""
        result = await subject_service.get_all(session)

        assert result is not None
        assert len(result) > 0
        assert all(isinstance(subject, Subject) for subject in result)

    @pytest.mark.asyncio
    async def test_get_subject_by_id(self, session: AsyncSession):
        """Test getting a subject by ID"""
        # First get a subject to test with
        subjects = await subject_service.get_all(session)
        subject_id = subjects[0].id

        result = await subject_service.get_by_id(session, subject_id)
        assert result is not None
        assert result.id == subject_id
        assert result.type is not None


class TestOrganizationService:
    """Test OrganizationService with real database"""

    @pytest.mark.asyncio
    async def test_get_organizations(self, session: AsyncSession):
        """Test getting all organizations"""
        result = await organization_service.get_all(session)

        assert result is not None
        assert len(result) > 0
        assert all(isinstance(org, Organization) for org in result)

    @pytest.mark.asyncio
    async def test_get_organization_by_id(self, session: AsyncSession):
        """Test getting an organization by ID"""
        # First get an organization to test with
        orgs = await organization_service.get_all(session)
        org_id = orgs[0].id

        result = await organization_service.get_by_id(session, org_id)
        assert result is not None
        assert result.id == org_id
        assert result.name is not None


class TestGradeService:
    """Test GradeService with real database"""

    @pytest.mark.asyncio
    async def test_get_grades(self, session: AsyncSession):
        """Test getting all grades"""
        result = await grade_service.get_all(session)

        assert result is not None
        assert len(result) > 0
        assert all(isinstance(grade, Grade) for grade in result)

    @pytest.mark.asyncio
    async def test_get_grade_by_id(self, session: AsyncSession):
        """Test getting a grade by ID"""
        # First get a grade to test with
        grades = await grade_service.get_all(session)
        grade_id = grades[0].id

        result = await grade_service.get_by_id(session, grade_id)
        assert result is not None
        assert result.id == grade_id
        assert result.grade is not None


class TestDifficultyService:
    """Test DifficultyService with real database"""

    @pytest.mark.asyncio
    async def test_get_difficulties(self, session: AsyncSession):
        """Test getting all difficulties"""
        result = await difficulty_service.get_all(session)

        assert result is not None
        assert len(result) > 0
        assert all(isinstance(difficulty, Difficulty) for difficulty in result)

    @pytest.mark.asyncio
    async def test_get_difficulty_by_id(self, session: AsyncSession):
        """Test getting a difficulty by ID"""
        # First get a difficulty to test with
        difficulties = await difficulty_service.get_all(session)
        difficulty_id = difficulties[0].id

        result = await difficulty_service.get_by_id(session, difficulty_id)
        assert result is not None
        assert result.id == difficulty_id
        assert result.type is not None


class TestErrorHandlingMiddleware:
    """Test error handling middleware"""

    import asyncio
    from fastapi import HTTPException
    from starlette.requests import Request
    from starlette.responses import Response

    @pytest.mark.asyncio
    async def test_http_exception_handled(self):
        async def call_next(request):
            raise HTTPException(status_code=404, detail='Not found')

        middleware = ErrorHandlingMiddleware(lambda x: x)
        request = Request(scope={'type': 'http', 'method': 'GET', 'path': '/test', 'headers': []})
        response = await middleware.dispatch(request, call_next)
        assert response.status_code == 404
        assert b'Not found' in response.body

    @pytest.mark.asyncio
    async def test_database_error_handled(self):
        async def call_next(request):
            raise DatabaseError(detail='DB failed')

        middleware = ErrorHandlingMiddleware(lambda x: x)
        request = Request(scope={'type': 'http', 'method': 'GET', 'path': '/test', 'headers': []})
        response = await middleware.dispatch(request, call_next)
        assert response.status_code == 500
        assert b'DB failed' in response.body

    @pytest.mark.asyncio
    async def test_unhandled_exception_propagates(self):
        async def call_next(request):
            raise ValueError('Test error')

        middleware = ErrorHandlingMiddleware(lambda x: x)
        request = Request(scope={'type': 'http', 'method': 'GET', 'path': '/test', 'headers': []})
        with pytest.raises(ValueError):
            await middleware.dispatch(request, call_next)


class TestModels:
    """Test model relationships and methods"""

    @pytest.mark.asyncio
    async def test_course_subject_relationships(self, session: AsyncSession):
        """Test course-subject relationships using ORM models"""
        from app.models import Course, Subject

        # Get a course ID first using ORM
        courses_result = await session.exec(select(Course.id))
        course_id = courses_result.scalar()
        if course_id:
            # Get the course using session.get
            course = await session.get(Course, course_id)
            assert course is not None
            assert course.id == course_id

            # Get subject links for this course
            links_result = await session.exec(select(CourseSubjectLink).where(CourseSubjectLink.course_id == course_id))
            subject_links = links_result.all()
            if subject_links:
                # Get subjects for this course
                subject_ids = [link.subject_id for link in subject_links if hasattr(link, 'subject_id')]
                if subject_ids:
                    # Get each subject using session.get
                    subjects = []
                    for subject_id in subject_ids:
                        subject = await session.get(Subject, subject_id)
                        if subject is not None:
                            subjects.append(subject)
                    assert len(subjects) == len(subject_ids)

    @pytest.mark.asyncio
    async def test_course_grade_relationships(self, session: AsyncSession):
        """Test course-grade relationships using ORM models"""
        from app.models import Course, Grade

        # Get a course ID first using ORM
        courses_result = await session.exec(select(Course.id))
        course_id = courses_result.scalar()
        if course_id:
            # Get the course using session.get
            course = await session.get(Course, course_id)
            assert course is not None
            assert course.id == course_id

            # Get grade links for this course
            links_result = await session.exec(select(CourseGradeLink).where(CourseGradeLink.course_id == course_id))
            grade_links = links_result.all()
            if grade_links:
                # Get grades for this course
                grade_ids = [link.grade_id for link in grade_links if hasattr(link, 'grade_id')]
                if grade_ids:
                    # Get each grade using session.get
                    grades = []
                    for grade_id in grade_ids:
                        grade = await session.get(Grade, grade_id)
                        if grade is not None:
                            grades.append(grade)
                    assert len(grades) == len(grade_ids)
