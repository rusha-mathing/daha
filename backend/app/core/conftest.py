import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

from main import app
from app.dependencies import get_session
from app.core.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.replace("test_db", "test_db_for_pytest")

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)


def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
