from pydantic import BaseModel


class CreditCardSchema(BaseModel):
    name: str
    limit: float
    cycle_day: int
    due_day: int
    currency: str


class CreditCardPublic(BaseModel):
    id: int
    name: str
    limit: float
    cycle_day: int
    due_day: int
    currency: str


class CreditCardUpdate(BaseModel):
    name: str
    limit: float
    cycle_day: int
    due_day: int


class ListCreditCards(BaseModel):
    credit_cards: list[CreditCardPublic]

