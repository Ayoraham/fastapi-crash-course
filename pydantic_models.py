from typing import List, Optional
from enum import IntEnum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

api = FastAPI()

class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512, description='Name of the todo')
    todo_description: str = Field(..., description='Description of the todo')
    priority: Priority = Field(default=Priority.LOW, description='Priority of the todo')


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    todo_id: int = Field(..., description = 'Unique identifier of the todo')


class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description='Name of todo')
    todo_description: Optional[str] = Field(None, description='Description of the todo')
    priority: Optional[Priority] = Field(None, description='Priority of the todo')


all_todos = [
    Todo(todo_id=1, todo_name="Sports", todo_description="Going to the gym for workout", priority=Priority.MEDIUM),
    Todo(todo_id=2, todo_name="Cleanup", todo_description="Cleaning the house", priority=Priority.HIGH),
    Todo(todo_id=3, todo_name="Memorize", todo_description="Memorize 1 page", priority=Priority.HIGH),
    Todo(todo_id=4, todo_name="Work", todo_description="Work on projects and hackathons", priority=Priority.MEDIUM),
    Todo(todo_id=5, todo_name="Development", todo_description="Build myself", priority=Priority.HIGH),
    Todo(todo_id=1, todo_name="Sleep", todo_description="Get some rest", priority=Priority.LOW),
]

# For every single endpoint, we can define a response model
# A response model is basically what the server should respond with


@api.get('/todos/{todo_id}', response_model= Todo)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
        
@api.get('/todos', response_model= List[Todo])
def get_todo(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos

@api.post('/todos', response_model= Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1 

    new_todo = Todo(todo_id= new_todo_id,
                    todo_name= todo.todo_name,
                    todo_description= todo.todo_description,
                    priority= todo.priority)
    all_todos.append(new_todo)
    return new_todo


@api.put('/todos', response_model= Todo)
def update_todos(todo_ind: int, todo_update: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_ind:
            if todo_update.todo_name is not None:
                todo.todo_name = todo_update.todo_name
            if todo_update.todo_description is not None:
                todo.todo_description = todo_update.todo_description
            if todo_update.priority is not None:
                todo.priority = todo_update.priority
            return todo
    raise HTTPException(status_code= 404, detail= 'Todo was not found')


@api.delete('/todos', response_model= Todo)
def delete_todos(todo_ind: int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id == todo_ind:
            deleted_todo = all_todos.pop(index)
            return deleted_todo
    
    raise HTTPException(status_code= 404, detail= 'Todo was not found')
            