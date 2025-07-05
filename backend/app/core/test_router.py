from datetime import date

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from psycopg import Connection
from pytest_postgresql import factories
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession

from app.models import Course, Subject, Organization, get_session, Difficulty, Grade, CourseSubjectLink, CourseGradeLink
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


@pytest.mark.asyncio
async def test_get_courses(client: AsyncClient):
    response = await client.get('/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    course_titles = [course['title'] for course in data]
    assert course_titles == ['Основы машинного обучения и нейронных сетей', 'Python Fundamentals']

    ai = data[0]
    assert ai['title'] == 'Основы машинного обучения и нейронных сетей'
    assert ai['url'] == 'https://practicum.yandex.ru/'
    assert ai['image_url'] == 'https://placehold.co/100x100'
    assert ai['subjects'] == ['ai', 'programming']
    assert ai['grades'] == [7, 8, 9]
    assert ai['start_date'] == '2023-09-01'
    assert ai['end_date'] == '2024-01-15'
    assert ai['difficulty'] == 'beginner'
    assert ai['description'] == 'Ведут специалисты из Яндекса с реальными кейсами из индустрии.'
    assert ai['organization'] == 'Coding Academy'


@pytest.mark.asyncio
async def test_get_course_not_found(client: AsyncClient):
    response = await client.get('/courses/1000/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Course not found'


@pytest.mark.asyncio
async def test_get_subjects(client: AsyncClient):
    response = await client.get('/subjects/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    subject_names = sorted([s['label'] for s in data])
    assert subject_names == sorted(['Искусственный интеллект', 'Робототехника', 'Программирование'])

    ai = next(s for s in data if s['label'] == 'Искусственный интеллект')
    assert ai['id'] is not None
    assert ai['label'] == 'Искусственный интеллект'
    assert (
        ai['icon']
        == '<path d="M20 9V7c0-1.1-.9-2-2-2h-3c0-1.66-1.34-3-3-3S9 3.34 9 5H6c-1.1 0-2 .9-2 2v2c-1.66 0-3 1.34-3 3s1.34 3 3 3v4c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-4c1.66 0 3-1.34 3-3s-1.34-3-3-3M7.5 11.5c0-.83.67-1.5 1.5-1.5s1.5.67 1.5 1.5S9.83 13 9 13s-1.5-.67-1.5-1.5M16 17H8v-2h8zm-1-4c-.83 0-1.5-.67-1.5-1.5S14.17 10 15 10s1.5.67 1.5 1.5S15.83 13 15 13"></path>'
    )
    assert ai['color'] == '#3f51b5'
    assert ai['additional_description'] == [
        'Слушатели осваивают практические навыки построения нейронных сетей и работы с большими данными.',
        'Курс включает работу с реальными проектами и актуальными инструментами искусственного интеллекта.',
    ]


@pytest.mark.asyncio
async def test_get_subject_success(client: AsyncClient, session: SQLModelAsyncSession):
    subject = (await session.exec(select(Subject).where(Subject.type == 'ai'))).first()
    response = await client.get(f'/subjects/{subject.id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['type'] == 'ai'
    assert data['label'] == 'Искусственный интеллект'
    assert (
        data['icon']
        == '<path d="M20 9V7c0-1.1-.9-2-2-2h-3c0-1.66-1.34-3-3-3S9 3.34 9 5H6c-1.1 0-2 .9-2 2v2c-1.66 0-3 1.34-3 3s1.34 3 3 3v4c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-4c1.66 0 3-1.34 3-3s-1.34-3-3-3M7.5 11.5c0-.83.67-1.5 1.5-1.5s1.5.67 1.5 1.5S9.83 13 9 13s-1.5-.67-1.5-1.5M16 17H8v-2h8zm-1-4c-.83 0-1.5-.67-1.5-1.5S14.17 10 15 10s1.5.67 1.5 1.5S15.83 13 15 13"></path>'
    )
    assert data['color'] == '#3f51b5'
    assert data['additional_description'] == [
        'Слушатели осваивают практические навыки построения нейронных сетей и работы с большими данными.',
        'Курс включает работу с реальными проектами и актуальными инструментами искусственного интеллекта.',
    ]


@pytest.mark.asyncio
async def test_get_subject_not_found(client: AsyncClient):
    response = await client.get('/subjects/999/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Subject not found'


@pytest.mark.asyncio
async def test_get_organizations(client: AsyncClient):
    response = await client.get('/organizations/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    org_names = sorted([o['name'] for o in data])
    assert org_names == ['Coding Academy', 'Science School']

    science_school = next(o for o in data if o['name'] == 'Science School')
    assert science_school['id'] is not None
    assert science_school['name'] == 'Science School'


@pytest.mark.asyncio
async def test_get_organization_success(client: AsyncClient, session: SQLModelAsyncSession):
    org = (await session.exec(select(Organization).where(Organization.name == 'Coding Academy'))).first()
    response = await client.get(f'/organizations/{org.id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Coding Academy'


@pytest.mark.asyncio
async def test_get_organization_not_found(client: AsyncClient):
    response = await client.get('/organizations/999/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Organization not found'


@pytest.mark.asyncio
async def test_subject_courses_relation(client: AsyncClient, session: SQLModelAsyncSession):
    subject = (await session.exec(select(Subject).where(Subject.type == 'programming'))).first()
    response = await client.get(f'/subjects/{subject.id}/')
    data = response.json()

    assert 'courses' not in data


@pytest.mark.asyncio
async def test_create_difficulty(client: AsyncClient, session: SQLModelAsyncSession):
    difficulty_data = {
        'type': 'NewDifficulty',
        'label': 'Новая сложность',
        'icon': 'new-difficulty-icon',
        'color': '#000000',
    }
    response = await client.post('/difficulties/', json=difficulty_data)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert isinstance(data['id'], int)
    difficulty = (await session.exec(select(Difficulty).where(Difficulty.id == data['id']))).first()
    assert difficulty.type == 'NewDifficulty'
    assert difficulty.label == 'Новая сложность'
    assert difficulty.icon == 'new-difficulty-icon'
    assert difficulty.color == '#000000'


@pytest.mark.asyncio
async def test_create_organization(client: AsyncClient, session: SQLModelAsyncSession):
    organization_data = {
        'name': 'New Organization',
    }
    response = await client.post('/organizations/', json=organization_data)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert isinstance(data['id'], int)
    org = (await session.exec(select(Organization).where(Organization.id == data['id']))).first()
    assert org.name == 'New Organization'


@pytest.mark.asyncio
async def test_create_grade(client: AsyncClient, session: SQLModelAsyncSession):
    grade_data = {
        'grade': 10,
    }
    response = await client.post('/grades/', json=grade_data)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert isinstance(data['id'], int)
    grade = (await session.exec(select(Grade).where(Grade.id == data['id']))).first()
    assert grade.grade == 10


@pytest.mark.asyncio
async def test_create_course(client: AsyncClient):
    course_data = {
        'title': 'New Course',
        'description': 'New Course Description',
        'start_date': '2024-01-01',
        'end_date': '2024-06-01',
        'url': 'https://example.com',
        'image_url': 'https://example.com/image.jpg',
        'organization': 'Coding Academy',
        'difficulty': 'beginner',
        'subjects': [],
        'grades': [],
    }
    response = await client.post('/courses/', json=course_data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'Course must have at least one subject'


@pytest.mark.asyncio
async def test_create_course_1(client: AsyncClient):
    course_data = {
        'title': 'title',
        'description': 'description',
        'start_date': '2024-01-01',
        'end_date': '2025-01-01',
        'url': 'https://example.com',
        'image_url': 'someimage',
        'grades': [6, 7, 8, 9],
        'difficulty': 'beginner',
        'subjects': ['programming', 'ai'],
        'organization': 'some org',
    }
    response = await client.post('/courses/', json=course_data)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert isinstance(data['id'], int)


@pytest.mark.asyncio
async def test_create_course_fail_grades(client: AsyncClient):
    course_data = {
        'title': 'New Course',
        'description': 'New Course Description',
        'start_date': '2024-01-01',
        'end_date': '2024-06-01',
        'url': 'https://example.com',
        'image_url': 'https://example.com/image.jpg',
        'organization': 'Coding Academy',
        'difficulty': 'beginner',
        'subjects': ['programming'],
        'grades': [6, 7, 8],
    }
    response = await client.post('/courses/', json=course_data)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert isinstance(data['id'], int)


@pytest.mark.asyncio
async def test_create_course_fail_subjects(client: AsyncClient):
    course_data = {
        'title': 'New Course',
        'description': 'New Course Description',
        'start_date': '2024-01-01',
        'end_date': '2024-06-01',
        'url': 'https://example.com',
        'image_url': 'https://example.com/image.jpg',
        'organization': 'Coding Academy',
        'difficulty': 'beginner',
        'subjects': ['programming', 'nonexistent'],
        'grades': [],
    }
    response = await client.post('/courses/', json=course_data)
    assert response.status_code == 404
    assert 'Subject nonexistent not found' in response.json()['detail']


@pytest.mark.asyncio
async def test_create_course_fail_subjects_mixed(client: AsyncClient):
    course_data = {
        'title': 'New Course',
        'description': 'New Course Description',
        'start_date': '2024-01-01',
        'end_date': '2024-06-01',
        'url': 'https://example.com',
        'image_url': 'https://example.com/image.jpg',
        'organization': 'Coding Academy',
        'difficulty': 'beginner',
        'subjects': ['nonexistent'],
        'grades': [],
    }
    response = await client.post('/courses/', json=course_data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'Subject nonexistent not found'


@pytest.mark.asyncio
async def test_create_subject(client: AsyncClient, session: SQLModelAsyncSession):
    subject_data = {
        'type': 'NewSubject',
        'label': 'Новый предмет',
        'icon': 'new-icon',
        'color': '#ffffff',
        'additional_description': ['Описание 1', 'Описание 2'],
    }
    response = await client.post('/subjects/', json=subject_data)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert isinstance(data['id'], int)
    subject = (await session.exec(select(Subject).where(Subject.id == data['id']))).first()
    assert subject.type == 'NewSubject'
    assert subject.label == 'Новый предмет'
    assert subject.icon == 'new-icon'
    assert subject.color == '#ffffff'
    assert subject.additional_description == ['Описание 1', 'Описание 2']


@pytest.mark.asyncio
async def test_update_subject_success(client: AsyncClient, session: SQLModelAsyncSession):
    create_response = await client.post(
        '/subjects/',
        json={
            'type': 'test_update',
            'label': 'Test Subject Update',
            'icon': 'test-icon',
            'color': '#cccccc',
            'additional_description': ['desc1', 'desc2'],
        },
    )
    assert create_response.status_code == 201
    response_data = create_response.json()
    assert 'id' in response_data
    assert isinstance(response_data['id'], int)
    created_subject_id = response_data['id']

    update_data = {
        'type': 'test_update_changed',
        'label': 'Updated Test Subject',
        'icon': 'updated-icon',
        'color': '#bbbbbb',
        'additional_description': ['new_desc1', 'new_desc2'],
    }

    response = await client.put(f'/subjects/{created_subject_id}', json=update_data)
    assert response.status_code == 200
    get_response = await client.get(f'/subjects/{created_subject_id}')
    assert get_response.status_code == 200
    updated_subject_data = get_response.json()

    assert updated_subject_data['type'] == update_data['type']
    assert updated_subject_data['label'] == update_data['label']
    assert updated_subject_data['icon'] == update_data['icon']
    assert updated_subject_data['color'] == update_data['color']
    assert updated_subject_data['additional_description'] == update_data['additional_description']

    db_subject = await session.get(Subject, created_subject_id)
    assert db_subject is not None
    assert db_subject.type == update_data['type']
    assert db_subject.label == update_data['label']
    assert db_subject.icon == update_data['icon']
    assert db_subject.color == update_data['color']
    assert db_subject.additional_description == update_data['additional_description']


@pytest.mark.asyncio
async def test_update_subject_not_found_1(client: AsyncClient):
    response = await client.put('/subjects/9999/', json={'type': 'nonexistent', 'label': 'Nonexistent'})
    assert response.status_code == 404
    assert response.json()['detail'] == 'Subject not found'


@pytest.mark.asyncio
async def test_delete_subject_success(client: AsyncClient, session: SQLModelAsyncSession):
    create_response = await client.post(
        '/subjects/',
        json={
            'type': 'test_delete',
            'label': 'Test Subject Delete',
            'icon': 'test-icon',
            'color': '#dddddd',
            'additional_description': ['desc_to_delete'],
        },
    )
    assert create_response.status_code == 201
    created_subject_id = create_response.json()['id']

    response = await client.delete(f'/subjects/{created_subject_id}')
    assert response.status_code == 204

    deleted_subject = await session.get(Subject, created_subject_id)
    assert deleted_subject is None


@pytest.mark.asyncio
async def test_update_subject_not_found(client: AsyncClient):
    valid_data = {
        'type': 'updated_type',
        'label': 'Updated Label',
    }
    response = await client.put('/subjects/9999/', json=valid_data)
    assert response.status_code == 404
    assert response.json()['detail'] == 'Subject not found'


@pytest.mark.asyncio
async def test_update_organization_success(client: AsyncClient, session: SQLModelAsyncSession):
    create_response = await client.post('/organizations/', json={'name': 'Original Org'})
    assert create_response.status_code == 201
    response_data = create_response.json()
    assert 'id' in response_data
    assert isinstance(response_data['id'], int)
    created_org_id = response_data['id']

    update_data = {'name': 'Updated Organization Name'}

    response = await client.put(f'/organizations/{created_org_id}', json=update_data)
    assert response.status_code == 200
    get_response = await client.get(f'/organizations/{created_org_id}')
    assert get_response.status_code == 200
    updated_org_data = get_response.json()

    assert updated_org_data['name'] == update_data['name']

    db_org = await session.get(Organization, created_org_id)
    assert db_org is not None
    assert db_org.name == update_data['name']


@pytest.mark.asyncio
async def test_update_organization_not_found(client: AsyncClient):
    response = await client.put('/organizations/9999/', json={'name': 'Nonexistent Org'})
    assert response.status_code == 404
    assert response.json()['detail'] == 'Organization not found'


@pytest.mark.asyncio
async def test_delete_organization_success(client: AsyncClient, session: SQLModelAsyncSession):
    create_response = await client.post('/organizations/', json={'name': 'Org To Delete'})
    assert create_response.status_code == 201
    created_org_id = create_response.json()['id']

    response = await client.delete(f'/organizations/{created_org_id}')
    assert response.status_code == 204

    db_org = await session.get(Organization, created_org_id)
    assert db_org is None


@pytest.mark.asyncio
async def test_delete_organization_not_found(client: AsyncClient):
    response = await client.delete('/organizations/9999/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Organization not found'


@pytest.mark.asyncio
async def test_update_grade_success(client: AsyncClient, session: SQLModelAsyncSession):
    create_response = await client.post('/grades/', json={'grade': 5})
    assert create_response.status_code == 201
    response_data = create_response.json()
    assert 'id' in response_data
    assert isinstance(response_data['id'], int)
    created_grade_id = response_data['id']

    update_data = {'grade': 11}

    response = await client.put(f'/grades/{created_grade_id}', json=update_data)
    assert response.status_code == 200
    get_response = await client.get(f'/grades/{created_grade_id}')
    assert get_response.status_code == 200
    updated_grade_data = get_response.json()

    assert updated_grade_data['grade'] == update_data['grade']

    db_grade = await session.get(Grade, created_grade_id)
    assert db_grade is not None
    assert db_grade.grade == update_data['grade']


@pytest.mark.asyncio
async def test_update_grade_not_found(client: AsyncClient):
    response = await client.put('/grades/9999/', json={'grade': 12})
    assert response.status_code == 404
    assert response.json()['detail'] == 'Grade not found'


@pytest.mark.asyncio
async def test_delete_grade_success(client: AsyncClient, session: SQLModelAsyncSession):
    create_response = await client.post('/grades/', json={'grade': 100})
    assert create_response.status_code == 201
    created_grade_id = create_response.json()['id']

    response = await client.delete(f'/grades/{created_grade_id}')
    assert response.status_code == 204

    db_grade = await session.get(Grade, created_grade_id)
    assert db_grade is None


@pytest.mark.asyncio
async def test_delete_grade_not_found(client: AsyncClient):
    response = await client.delete('/grades/9999/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Grade not found'


@pytest.mark.asyncio
async def test_update_difficulty_success(client: AsyncClient, session: SQLModelAsyncSession):
    create_response = await client.post(
        '/difficulties/',
        json={'type': 'original_difficulty', 'label': 'Original Label', 'icon': 'original_icon', 'color': '#aabbcc'},
    )
    assert create_response.status_code == 201
    response_data = create_response.json()
    assert 'id' in response_data
    assert isinstance(response_data['id'], int)
    created_difficulty_id = response_data['id']

    update_data = {'type': 'updated_difficulty', 'label': 'Updated Label', 'icon': 'updated_icon', 'color': '#ddeeff'}

    response = await client.put(f'/difficulties/{created_difficulty_id}', json=update_data)
    assert response.status_code == 200
    get_response = await client.get(f'/difficulties/{created_difficulty_id}')
    assert get_response.status_code == 200
    updated_difficulty_data = get_response.json()

    assert updated_difficulty_data['type'] == update_data['type']
    assert updated_difficulty_data['label'] == update_data['label']
    assert updated_difficulty_data['icon'] == update_data['icon']
    assert updated_difficulty_data['color'] == update_data['color']

    db_difficulty = await session.get(Difficulty, created_difficulty_id)
    assert db_difficulty is not None
    assert db_difficulty.type == update_data['type']
    assert db_difficulty.label == update_data['label']
    assert db_difficulty.icon == update_data['icon']
    assert db_difficulty.color == update_data['color']


@pytest.mark.asyncio
async def test_update_difficulty_not_found(client: AsyncClient):
    response = await client.put('/difficulties/9999/', json={'type': 'nonexistent', 'label': 'Nonexistent'})
    assert response.status_code == 404
    assert response.json()['detail'] == 'Difficulty not found'


@pytest.mark.asyncio
async def test_delete_difficulty_success(client: AsyncClient, session: SQLModelAsyncSession):
    create_response = await client.post(
        '/difficulties/',
        json={
            'type': 'difficulty_to_delete',
            'label': 'Difficulty Delete Label',
            'icon': 'delete_icon',
            'color': '#112233',
        },
    )
    assert create_response.status_code == 201
    created_difficulty_id = create_response.json()['id']

    response = await client.delete(f'/difficulties/{created_difficulty_id}')
    assert response.status_code == 204

    db_difficulty = await session.get(Difficulty, created_difficulty_id)
    assert db_difficulty is None


@pytest.mark.asyncio
async def test_delete_difficulty_not_found(client: AsyncClient):
    response = await client.delete('/difficulties/9999/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Difficulty not found'


@pytest.mark.asyncio
async def test_update_course_success(client: AsyncClient, session: SQLModelAsyncSession):
    response = await client.get('/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    course_to_update_id = data[0]['id']

    update_data = {
        'title': 'Updated Course Title',
        'description': 'Updated Course Description',
        'start_date': '2025-01-01',
        'end_date': '2025-12-31',
        'url': 'https://updated.example.com',
        'image_url': 'https://updated.example.com/image.jpg',
        'organization': 'Science School',
        'difficulty': 'beginner',
        'subjects': ['ai'],
        'grades': [7, 100],
    }

    response = await client.put(f'/courses/{course_to_update_id}', json=update_data)
    assert response.status_code == 200

    get_response = await client.get(f'/courses/{course_to_update_id}')
    assert get_response.status_code == 200
    updated_course_data = get_response.json()

    assert updated_course_data['title'] == update_data['title']
    assert updated_course_data['description'] == update_data['description']
    assert updated_course_data['start_date'] == update_data['start_date']
    assert updated_course_data['end_date'] == update_data['end_date']
    assert updated_course_data['url'] == update_data['url']
    assert updated_course_data['image_url'] == update_data['image_url']
    assert updated_course_data['organization'] == update_data['organization']
    assert updated_course_data['difficulty'] == update_data['difficulty']
    assert sorted(updated_course_data['subjects']) == sorted(update_data['subjects'])
    assert sorted(updated_course_data['grades']) == sorted(update_data['grades'])

    db_course_after_update = await session.get(Course, course_to_update_id)
    assert db_course_after_update is not None
    assert db_course_after_update.title == update_data['title']

    org_after_update = (await session.exec(select(Organization).where(Organization.name == 'Science School'))).first()
    assert db_course_after_update.organization.id == org_after_update.id

    difficulty_after_update = (await session.exec(select(Difficulty).where(Difficulty.type == 'beginner'))).first()
    assert db_course_after_update.difficulty.id == difficulty_after_update.id


@pytest.mark.asyncio
async def test_update_course_not_found(client: AsyncClient):
    response = await client.put(
        '/courses/9999/',
        json={
            'title': 'Nonexistent',
            'description': '...',
            'start_date': '2024-01-01',
            'end_date': '2024-06-01',
            'url': '',
            'image_url': '',
            'organization': 'Coding Academy',
            'difficulty': 'beginner',
            'subjects': [],
            'grades': [],
        },
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'Course not found'


@pytest.mark.asyncio
async def test_update_course_fail_on_missing_related_entity(client: AsyncClient):
    courses_response = await client.get('/courses/')
    assert courses_response.status_code == 200
    courses_data = courses_response.json()
    assert len(courses_data) >= 1
    course_to_update_id = courses_data[0]['id']

    update_data_invalid_difficulty = {
        'title': 'Invalid Diff Course',
        'description': '...',
        'start_date': '2024-01-01',
        'end_date': '2024-06-01',
        'url': '',
        'image_url': '',
        'organization': 'Coding Academy',
        'difficulty': 'nonexistent_difficulty',
        'subjects': ['ai'],
        'grades': [7],
    }
    response_invalid_diff = await client.put(f'/courses/{course_to_update_id}', json=update_data_invalid_difficulty)
    assert response_invalid_diff.status_code == 400
    assert response_invalid_diff.json()['detail'] == 'Difficulty not found'

    update_data_invalid_subject = {
        'title': 'Invalid Subj Course',
        'description': '...',
        'start_date': '2024-01-01',
        'end_date': '2024-06-01',
        'url': '',
        'image_url': '',
        'organization': 'Coding Academy',
        'difficulty': 'beginner',
        'subjects': ['ai', 'nonexistent_subject'],
        'grades': [7],
    }
    response_invalid_subj = await client.put(f'/courses/{course_to_update_id}', json=update_data_invalid_subject)
    assert response_invalid_subj.status_code == 400
    assert response_invalid_subj.json()['detail'] == "Subjects not found: ['nonexistent_subject']"

    update_data_invalid_grade = {
        'title': 'Invalid Grade Course',
        'description': '...',
        'start_date': '2024-01-01',
        'end_date': '2024-06-01',
        'url': '',
        'image_url': '',
        'organization': 'Coding Academy',
        'difficulty': 'beginner',
        'subjects': ['ai'],
        'grades': [7, 999],
    }
    response_invalid_grade = await client.put(f'/courses/{course_to_update_id}', json=update_data_invalid_grade)
    assert response_invalid_grade.status_code == 200

    update_data_invalid_org = {
        'title': 'Invalid Org Course',
        'description': '...',
        'start_date': '2024-01-01',
        'end_date': '2024-06-01',
        'url': '',
        'image_url': '',
        'organization': 'Nonexistent Organization',
        'difficulty': 'beginner',
        'subjects': ['ai'],
        'grades': [7],
    }
    response_invalid_org = await client.put(f'/courses/{course_to_update_id}', json=update_data_invalid_org)
    assert response_invalid_org.status_code == 200


@pytest.mark.asyncio
async def test_delete_course_success(client: AsyncClient, session: SQLModelAsyncSession):
    course_create_data = {
        'title': 'Course to Delete',
        'description': 'This course will be deleted',
        'start_date': '2026-01-01',
        'end_date': '2026-12-31',
        'url': 'https://delete.example.com',
        'image_url': 'https://delete.example.com/image.jpg',
        'organization': 'Org To Be Deleted From',
        'difficulty': 'beginner',
        'subjects': ['programming'],
        'grades': [8],
    }
    create_response = await client.post('/courses/', json=course_create_data)
    assert create_response.status_code == 201
    created_course_id = create_response.json()['id']

    response = await client.delete(f'/courses/{created_course_id}')
    assert response.status_code == 204

    deleted_course = await session.get(Course, created_course_id)
    assert deleted_course is None

    links = await session.exec(select(CourseSubjectLink).where(CourseSubjectLink.course_id == created_course_id))
    assert links.first() is None

    grade_links = await session.exec(select(CourseGradeLink).where(CourseGradeLink.course_id == created_course_id))
    assert grade_links.first() is None


@pytest.mark.asyncio
async def test_delete_course_not_found(client: AsyncClient):
    response = await client.delete('/courses/9999/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Course not found'
