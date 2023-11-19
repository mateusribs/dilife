from fastapi import FastAPI

from dilife.routes import accounts, auth, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(accounts.router)


@app.get('/')
def read_root():
    return {'message': 'Hello World'}
