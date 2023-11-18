from sqlalchemy import select
from sqlalchemy.orm import Session

from dilife.models import Account, User


def test_create_user(session):
    new_user = User(username='foo', password='secret123', email='foo@bar.com')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'foo'))

    assert user.username == 'foo'


def test_create_account(session: Session, user: User):
    account = Account(
        name='account test', user_id=user.id, balance=1000.60, currency='BRL'
    )

    session.add(account)
    session.commit()
    session.refresh(account)

    user = session.scalar(select(User).where(User.id == user.id))

    assert account in user.accounts
