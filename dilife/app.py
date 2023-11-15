from fastapi import FastAPI

from dilife.schemas import UserPublic, UserSchema

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Hello World'}


@app.post('/users/', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema):
    return user
