from sqlalchemy import select

from dilife.models import User


def test_create_user(session):
    new_user = User(username='foo', password='secret123', email='foo@bar.com')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'foo'))

    assert user.username == 'foo'
