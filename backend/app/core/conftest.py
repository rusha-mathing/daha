import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from psycopg import Connection
from pytest_postgresql import factories
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession
from datetime import date
from app.models import Subject, Organization, Difficulty, Grade, Course, CourseSubjectLink, CourseGradeLink, get_session
from main import api

postgresql_proc = factories.postgresql_proc(dbname='test_db')
postgresql = factories.postgresql('postgresql_proc')


@pytest_asyncio.fixture(name='session')
async def session_fixture(postgresql: Connection):
    engine = create_async_engine(
        f'postgresql+asyncpg://'
        f'{postgresql.info.user}:'
        f'{postgresql.info.password}@'
        f'{postgresql.info.host}:{postgresql.info.port}/'
        f'{postgresql.info.dbname}'
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with SQLModelAsyncSession(bind=engine, expire_on_commit=False) as local_session:
        ai = Subject(
            type='ai',
            label='Искусственный интеллект',
            icon='<path d="M20 9V7c0-1.1-.9-2-2-2h-3c0-1.66-1.34-3-3-3S9 3.34 9 5H6c-1.1 0-2 .9-2 2v2c-1.66 0-3 1.34-3 3s1.34 3 3 3v4c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-4c1.66 0 3-1.34 3-3s-1.34-3-3-3M7.5 11.5c0-.83.67-1.5 1.5-1.5s1.5.67 1.5 1.5S9.83 13 9 13s-1.5-.67-1.5-1.5M16 17H8v-2h8zm-1-4c-.83 0-1.5-.67-1.5-1.5S14.17 10 15 10s1.5.67 1.5 1.5S15.83 13 15 13"></path>',
            color='#3f51b5',
            additional_description=[
                'Слушатели осваивают практические навыки построения нейронных сетей и работы с большими данными.',
                'Курс включает работу с реальными проектами и актуальными инструментами искусственного интеллекта.',
            ],
        )
        robotics = Subject(
            type='robotics',
            label='Робототехника',
            icon='<path d="m19.93 8.21-3.6 1.68L14 7.7V6.3l2.33-2.19 3.6 1.68c.38.18.82.01 1-.36.18-.38.01-.82-.36-1L16.65 2.6c-.38-.18-.83-.1-1.13.2l-1.74 1.6c-.18-.24-.46-.4-.78-.4-.55 0-1 .45-1 1v1H8.82C8.34 4.65 6.98 3.73 5.4 4.07c-1.16.25-2.15 1.25-2.36 2.43-.22 1.32.46 2.47 1.48 3.08L7.08 18H4v3h13v-3h-3.62L8.41 8.77c.17-.24.31-.49.41-.77H12v1c0 .55.45 1 1 1 .32 0 .6-.16.78-.4l1.74 1.6c.3.3.75.38 1.13.2l3.92-1.83c.38-.18.54-.62.36-1-.18-.37-.62-.54-1-.36M6 8c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1"></path>',
            color='#9c27b0',
            additional_description=[
                'Слушатели осваивают практические навыки построения нейронных сетей и работы с большими данными.',
                'Курс включает работу с реальными проектами и актуальными инструментами искусственного интеллекта.',
            ],
        )
        programming = Subject(
            type='programming',
            label='Программирование',
            icon='<path d="M9.4 16.6 4.8 12l4.6-4.6L8 6l-6 6 6 6zm5.2 0 4.6-4.6-4.6-4.6L16 6l6 6-6 6z"></path>',
            color='#00bfa5',
            additional_description=[
                'Обучение строится на решении практических задач с постепенным повышением сложности.',
                'Участники научатся писать оптимальный и читаемый код, работая над реальными проектами.',
            ],
        )
        local_session.add_all([ai, robotics, programming])
        await local_session.commit()
        org1 = Organization(name='Coding Academy')
        org2 = Organization(name='Science School')
        local_session.add_all([org1, org2])
        await local_session.commit()

        beginner = Difficulty(
            type='beginner',
            label='начальный',
            icon='<path d="M5 13.18v4L12 21l7-3.82v-4L12 17zM12 3 1 9l11 6 9-4.91V17h2V9z"></path>',
            color='#4caf50',
        )
        local_session.add(beginner)
        await local_session.commit()

        grade_7 = Grade(grade=7)
        grade_8 = Grade(grade=8)
        grade_9 = Grade(grade=9)
        local_session.add_all([grade_7, grade_8, grade_9])
        await local_session.commit()
        ai_subject_ids = [ai.id, programming.id]
        ai_grade_ids = [grade_7.id, grade_8.id, grade_9.id]

        ai_course = Course(
            title='Основы машинного обучения и нейронных сетей',
            description='Ведут специалисты из Яндекса с реальными кейсами из индустрии.',
            start_date=date(2023, 9, 1),
            end_date=date(2024, 1, 15),
            url='https://practicum.yandex.ru/',
            image_url='https://placehold.co/100x100',
            organization_id=org1.id,
            difficulty_id=beginner.id,
            subject_ids=ai_subject_ids,
            grade_ids=ai_grade_ids,
        )
        local_session.add(ai_course)
        await local_session.commit()  # .id

        for subject_id in ai_subject_ids:
            local_session.add(CourseSubjectLink(course_id=ai_course.id, subject_id=subject_id))
        for grade_id in ai_grade_ids:
            local_session.add(CourseGradeLink(course_id=ai_course.id, grade_id=grade_id))
        await local_session.commit()
        python_f_subject_ids = [programming.id]
        python_f_grade_ids = [grade_7.id, grade_8.id, grade_9.id]

        python_fundementals_course = Course(
            title='Python Fundamentals',
            description='Learn Python programming',
            start_date=date(2023, 10, 1),
            end_date=date(2024, 3, 1),
            url='https://example.com/python',
            image_url='https://placehold.co/100x100',
            organization_id=org1.id,
            difficulty_id=beginner.id,
            subject_ids=python_f_subject_ids,
            grade_ids=python_f_grade_ids,
        )
        local_session.add(python_fundementals_course)
        await local_session.commit()  # .id

        for subject_id in python_f_subject_ids:
            local_session.add(CourseSubjectLink(course_id=python_fundementals_course.id, subject_id=subject_id))
        for grade_id in python_f_grade_ids:
            local_session.add(CourseGradeLink(course_id=python_fundementals_course.id, grade_id=grade_id))
        await local_session.commit()
        yield local_session
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(name='client')
async def client_fixture(session: SQLModelAsyncSession):
    async def get_session_override():
        return session

    api.dependency_overrides[get_session] = get_session_override
    async with AsyncClient(transport=ASGITransport(api), base_url='http://test', follow_redirects=True) as ac:
        yield ac
    api.dependency_overrides.clear()
