from datetime import date

from fastapi.testclient import TestClient
import pytest
from sqlmodel import create_engine, SQLModel, StaticPool, Session, select

from app.models import Course, Subject, Organization, get_session
from main import api


@pytest.fixture(name='session')
def session_fixture():
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        math = Subject(name='Mathematics')
        physics = Subject(name='Physics')
        programming = Subject(name='Programming')
        session.add_all([math, physics, programming])
        session.commit()

        org1 = Organization(name='Coding Academy')
        org2 = Organization(name='Science School')
        session.add_all([org1, org2])
        session.commit()

        courses = [
            Course(
                name='Algebra Basics',
                url='https://example.com/algebra',
                organization_id=org1.id,
                subject_id=math.id,
                min_class=5,
                max_class=8,
                start=date(2023, 9, 1),
                end=date(2024, 1, 15),
                difficulty=2,
                description='Introduction to algebra',
            ),
            Course(
                name='Python Fundamentals',
                url='https://example.com/python',
                organization_id=org1.id,
                subject_id=programming.id,
                min_class=7,
                max_class=11,
                start=date(2023, 10, 1),
                end=date(2024, 3, 1),
                difficulty=3,
                description='Learn Python programming',
            ),
            Course(
                name='Physics for Beginners',
                url='https://example.com/physics',
                organization_id=org2.id,
                subject_id=physics.id,
                min_class=6,
                max_class=9,
                start=date(2023, 9, 15),
                end=date(2024, 2, 28),
                difficulty=3,
                description='Basic physics concepts',
            ),
        ]
        session.add_all(courses)
        session.commit()
        yield session


@pytest.fixture(name='client')
def client_fixture(session: Session):
    def get_session_override():
        return session

    api.dependency_overrides[get_session] = get_session_override
    client = TestClient(api)
    yield client
    api.dependency_overrides.clear()


def test_get_courses(client: TestClient):
    response = client.get('/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    course_names = [course['name'] for course in data]
    assert course_names == ['Algebra Basics', 'Python Fundamentals', 'Physics for Beginners']

    algebra = data[0]
    assert algebra['name'] == 'Algebra Basics'
    assert algebra['url'] == 'https://example.com/algebra'
    assert algebra['min_class'] == 5
    assert algebra['max_class'] == 8
    assert algebra['start'] == '2023-09-01'
    assert algebra['end'] == '2024-01-15'
    assert algebra['difficulty'] == 2
    assert algebra['description'] == 'Introduction to algebra'
    assert algebra['organization']['name'] == 'Coding Academy'
    assert algebra['subject']['name'] == 'Mathematics'


def test_get_course_success(client: TestClient, session: Session):
    course = session.exec(select(Course).where(Course.name == 'Python Fundamentals')).first()

    response = client.get(f'/courses/{course.id}/')
    assert response.status_code == 200
    data = response.json()

    assert data['name'] == 'Python Fundamentals'
    assert data['url'] == 'https://example.com/python'
    assert data['min_class'] == 7
    assert data['max_class'] == 11
    assert data['start'] == '2023-10-01'
    assert data['end'] == '2024-03-01'
    assert data['difficulty'] == 3
    assert data['description'] == 'Learn Python programming'
    assert data['organization']['name'] == 'Coding Academy'
    assert data['subject']['name'] == 'Programming'


def test_get_course_not_found(client: TestClient):
    response = client.get('/courses/1000/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Course not found'


# Тесты для /subjects/
def test_get_subjects(client: TestClient):
    response = client.get('/subjects/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    subject_names = sorted([s['name'] for s in data])
    assert subject_names == ['Mathematics', 'Physics', 'Programming']

    # Проверяем первый предмет
    math = next(s for s in data if s['name'] == 'Mathematics')
    assert math['id'] is not None
    assert math['name'] == 'Mathematics'


def test_get_subject_success(client: TestClient, session: Session):
    subject = session.exec(select(Subject).where(Subject.name == 'Physics')).first()
    response = client.get(f'/subjects/{subject.id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Physics'


def test_get_subject_not_found(client: TestClient):
    response = client.get('/subjects/999/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Subject not found'


# Тесты для /organizations/
def test_get_organizations(client: TestClient):
    response = client.get('/organizations/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    org_names = sorted([o['name'] for o in data])
    assert org_names == ['Coding Academy', 'Science School']

    # Проверяем организацию
    science_school = next(o for o in data if o['name'] == 'Science School')
    assert science_school['id'] is not None
    assert science_school['name'] == 'Science School'


def test_get_organization_success(client: TestClient, session: Session):
    org = session.exec(select(Organization).where(Organization.name == 'Coding Academy')).first()
    response = client.get(f'/organizations/{org.id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Coding Academy'


def test_get_organization_not_found(client: TestClient):
    response = client.get('/organizations/999/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Organization not found'


def test_organization_courses_relation(client: TestClient, session: Session):
    org = session.exec(select(Organization).where(Organization.name == 'Coding Academy')).first()
    response = client.get(f'/organizations/{org.id}/')
    data = response.json()

    assert 'courses' not in data


def test_subject_courses_relation(client: TestClient, session: Session):
    subject = session.exec(select(Subject).where(Subject.name == 'Programming')).first()
    response = client.get(f'/subjects/{subject.id}/')
    data = response.json()

    assert 'courses' not in data
