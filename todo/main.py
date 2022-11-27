from typing import Optional

from fastapi import FastAPI
from config import settings

from todo.models.models import Todo, Todo_Pydantic, ToDoIn_Pydantic
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise


app = FastAPI()

@app.get('/')
async def read_root():
    return {"Hello": "World"}

class Status(BaseModel):
    message: str

"""
set the url and model for post request
async create the todo object and await from orm
"""
@app.post('/todos', response_model=Todo_Pydantic)
async def create_todo(todo: ToDoIn_Pydantic):
    todo_obj = await Todo.create(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_tortoise_orm(todo_obj)


register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={'models': ["todo.models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)