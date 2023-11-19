from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.types import Message

from dilife.database import get_session
from dilife.models import Account, User
from dilife.schemas.account import (
    AccountPublic,
    AccountSchema,
    AccountUpdate,
    ListAccount,
)
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


@router.patch('/{account_id}', status_code=200, response_model=AccountPublic)
def update_account(
    user: CurrentUser,
    session: Session,
    account: AccountUpdate,
    account_id: int,
):
    db_account = session.scalar(
        select(Account).where(
            Account.id == account_id, Account.user_id == user.id
        )
    )

    if not db_account:
        raise HTTPException(status_code=404, detail='account not found')

    for key, value in account.model_dump(exclude_unset=True).items():
        setattr(db_account, key, value)

    session.add(db_account)
    session.commit()
    session.refresh(db_account)

    return db_account


@router.delete('/{account_id}', response_model=Message)
def delete_account(
    account_id: int,
    session: Session,
    user: CurrentUser,
):
    account = session.scalar(
        select(Account).where(
            Account.id == account_id, Account.user_id == user.id
        )
    )

    if not account:
        raise HTTPException(status_code=404, detail='account not found')

    session.delete(account)
    session.commit()

    return {'detail': 'account deleted'}
