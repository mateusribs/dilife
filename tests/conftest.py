import factory
import factory.fuzzy
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from dilife.app import app
from dilife.database import get_session
from dilife.models import Account, Base, CreditCard, Currency, User
from dilife.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = factory.LazyAttribute(lambda obj: f'test{obj.id}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}secret2')


class AccountFactory(factory.Factory):
    class Meta:
        model = Account

    name = factory.Faker('text')
    balance = factory.fuzzy.FuzzyDecimal(low=10, high=4000, precision=2)
    currency = factory.fuzzy.FuzzyChoice(Currency)
    user_id = 1


class CreditCardFactory(factory.Factory):
    class Meta:
        model = CreditCard

    name = factory.Faker('text')
    limit = factory.fuzzy.FuzzyInteger(low=10, high=3000)
    cycle_day = factory.fuzzy.FuzzyInteger(low=1, high=30)
    due_day = factory.fuzzy.FuzzyInteger(low=1, high=30)
    currency = factory.fuzzy.FuzzyChoice(Currency)
    user_id = 1


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
    user = UserFactory(password=get_password_hash('secret123'))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'secret123'

    return user


@fixture
def other_user(session):
    user = UserFactory(password=get_password_hash('anothersecret123'))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'anothersecret123'

    return user


@fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']
