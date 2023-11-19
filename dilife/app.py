from fastapi import FastAPI

from dilife.routes import accounts, auth, credit_cards, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(credit_cards.router)


@app.get('/')
def read_root():
    return {'message': 'Hello World'}
