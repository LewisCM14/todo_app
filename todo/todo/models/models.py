from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Todo(models.Model):
    """
    The model to hold the todo items
    """
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    completed = fields.BooleanField()

Todo_Pydantic = pydantic_model_creator(Todo, name="Todo")
ToDoIn_Pydantic = pydantic_model_creator(Todo, name="TodoIn", exclude_readonly=True)
