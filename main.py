from fastapi import FastAPI, Path, HTTPException, Request
from pydantic import BaseModel
from typing import Annotated, List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


app = FastAPI()
templates = Jinja2Templates(directory="templates") 

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int

@app.get('/')
async def welcome(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})

@app.get('/user/{user_id}')
async def get_user(request: Request, user_id: Annotated[int, Path(gt=0)]) -> HTMLResponse:
    try:
        for user in users:
            if user.id == user_id:
                return templates.TemplateResponse('users.html', {'request': request, 'user': user})
    except IndexError:
        raise HTTPException(status_code=404, details='User was not found')

@app.get('/users')
async def get_all_users() -> List[User]:
    return users

@app.post('/user/{username}/{age}')
async def create_user(
        username: Annotated[str, Path(min_length=2, max_length=20, regex="^[a-zA-Z0-9_-]+$")],
        age: Annotated[int, Path(gt=0, lt=100)]
    ) -> User:
    user_id = len(users) + 1 if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user

@app.put('/user/{user_id}/{username}/{age}')
async def update_user_info(
        user_id: Annotated[int, Path(gt=0)], 
        username: Annotated[str, Path(min_length=2,
                                    max_length=20,
                                    regex="^[a-zA-Z0-9_-]+$")],
        age: Annotated[int, Path(gt=0, lt=100)]
    ) -> User:
    try:
        for user in users:
            if user.id == user_id:
                user.username = username
                user.age = age
                return user 
    except IndexError:
        raise HTTPException(status_code=404, details='User was not found')

@app.delete('/user/{user_id}')
async def delete_message(user_id: Annotated[int, Path(gt=0)],) -> str:
    try:
        for user in users:
            if user.id == user_id:
                users.remove(user)
                return user
    except IndexError:
        raise HTTPException(status_code=404, details='User was not found')    