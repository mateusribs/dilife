from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from dilife.app import app
from dilife.database import get_session
from dilife.models import Base, User


@fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)


@fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@fixture
def user(session):
    user = User(username='foo', email='foo@bar.com', password='secret123')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
