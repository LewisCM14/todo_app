from typing import Optional, List
 
from fastapi import FastAPI, HTTPException
from todo.models.models import Todo, Todo_Pydantic, TodoIn_Pydantic
from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from config import settings
app = FastAPI()

class Status(BaseModel):
    message: str

@app.get('/')
async def read_root():
    return {"Hello": "World"}

"""
GET a list of items asynchronously from the Todo model.
"""
@app.get('/todos', response_model=List[Todo_Pydantic])
async def get_todos():
    return await Todo_Pydantic.from_queryset(Todo.all())

"""
GET specific items from the Todo model via ID.
Triggers 404 error if request invalid.
"""
@app.get("/todos/{todo_id}", response_model=Todo_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_todo(todo_id: int):
    return await Todo_Pydantic.from_queryset_single(Todo.get(id = todo_id))

"""
POST JSON objects to the Todo model asynchronously via tortoise orm
"""
@app.post("/todos", response_model=Todo_Pydantic)
async def create_todo(todo: TodoIn_Pydantic):
    todo_obj = await Todo.create(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_tortoise_orm(todo_obj)


register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["todo.models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)