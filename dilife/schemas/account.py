from pydantic import BaseModel


class AccountSchema(BaseModel):
    name: str
    balance: float
    currency: str


class AccountPublic(BaseModel):
    id: int
    name: str
    balance: float
    currency: str


class AccountUpdate(BaseModel):
    name: str | None = None
    currency: str | None = None


class ListAccount(BaseModel):
    accounts: list[AccountPublic]
