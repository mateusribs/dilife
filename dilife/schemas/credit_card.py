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
    name: str | None = None
    limit: float | None = None
    cycle_day: int | None = None
    due_day: int | None = None


class ListCreditCards(BaseModel):
    credit_cards: list[CreditCardPublic]
