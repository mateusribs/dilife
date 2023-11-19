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


class ListAccount(BaseModel):
    accounts: list[AccountPublic]
