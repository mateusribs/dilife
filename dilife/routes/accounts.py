from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dilife.database import get_session
from dilife.models import Account, User
from dilife.schemas.account import AccountPublic, AccountSchema
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
