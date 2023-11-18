from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from dilife.app import app
from dilife.database import get_session
from dilife.models import Base, User
from dilife.security import get_password_hash


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
    user = User(
        username='foo',
        email='foo@bar.com',
        password=get_password_hash('secret123'),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'secret123'

    return user


@fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']
