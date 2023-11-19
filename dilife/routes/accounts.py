from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from dilife.database import get_session
from dilife.models import Account, User
from dilife.schemas.account import AccountPublic, AccountSchema, ListAccount
from dilife.security import get_current_user

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


router = APIRouter(prefix='/accounts', tags=['accounts'])


@router.post('/', status_code=201, response_model=AccountPublic)
def create_account(
    account: AccountSchema, user: CurrentUser, session: Session
):
    db_account: Account = Account(
        name=account.name,
        balance=account.balance,
        currency=account.currency,
        user_id=user.id,
    )

    session.add(db_account)
    session.commit()
    session.refresh(db_account)

    return db_account


@router.get('/', status_code=200, response_model=ListAccount)
def get_accounts_list(
    user: CurrentUser,
    session: Session,
    currency: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Account).where(Account.user_id == user.id)

    if currency:
        query = query.filter(Account.currency == currency)

    accounts = session.scalars(query.offset(offset).limit(limit)).all()

    return {'accounts': accounts}
