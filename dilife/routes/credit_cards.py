from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from dilife.database import get_session
from dilife.models import CreditCard, User
from dilife.schemas.credit_card import (
    CreditCardPublic,
    CreditCardSchema,
    ListCreditCards,
)
from dilife.security import get_current_user

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/credit_cards', tags=['credit_cards'])


@router.post('/', status_code=201, response_model=CreditCardPublic)
def create_credit_card(
    user: CurrentUser, session: Session, credit_card: CreditCardSchema
):
    db_credit_card: CreditCard = CreditCard(
        name=credit_card.name,
        user_id=user.id,
        limit=credit_card.limit,
        cycle_day=credit_card.cycle_day,
        due_day=credit_card.due_day,
        currency=credit_card.currency,
    )

    session.add(db_credit_card)
    session.commit()
    session.refresh(db_credit_card)

    return db_credit_card


@router.get('/', status_code=200, response_model=ListCreditCards)
def get_credit_cards_list(
    user: CurrentUser,
    session: Session,
    offset: int = Query(None),
    limit: int = Query(None),
):

    query = select(CreditCard).where(CreditCard.user_id == user.id)

    credit_cards = session.scalars(query.offset(offset).limit(limit)).all()

    return {'credit_cards': credit_cards}