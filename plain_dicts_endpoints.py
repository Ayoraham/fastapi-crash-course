from fastapi import FastAPI

api = FastAPI()

# Define Endpoints 
# There are 4 types of http methods - GET , POST,  PUT ,  DELETE
# GET is fetching info from the http, POST is adding smth new to it
# PUT is replacing smth in it and DELETE is removing

@api.get('/')
def index():
    return{"message": "Hello World"}


# Making api endpoints for a to=do
#preparing basic database for endpoints te communicate with

all_todos = [
    {"todo_id":1, "todo_name": "Sports", "todo_description": "Go to the gym"},
    {"todo_id":2, "todo_name": "Read", "todo_description": "Study for exams"},
    {"todo_id":3, "todo_name": "Shop", "todo_description": "Buy stuff"},
    {"todo_id":4, "todo_name": "Memorize", "todo_description": "Memorize 1 page"},
    {"todo_id":5, "todo_name": "Rest", "todo_description": "Sleep 40 mins"},
]

# Endpoint to fetch single todos        
# Using path parameter here - they're compulsory, 
# FastAPI willl return not found if not there                                                                                                                                                                                                                                                             
@api.get('/todos/{todo_id}')
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            return {"result": todo}
        

# Endpoint to fetch specific todos
# Query parameter - optional, added after qeustion mark                                                                                                                                                                                                                                                                    
@api.get('/todos')
def get_todo(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos
    

# Posting
@api.post('/todos')
def create_todo(todo:dict):
    new_todo_id = max(todo['todo_id'] for todo in all_todos) + 1 

    new_todo = {
        'todo_id': new_todo_id,
        'todo_name': todo['todo_name'],
        'todo_description': todo['todo_description']
    }

    all_todos.append(new_todo)
    return new_todo


# Put/Update endpoint
@api.put('/todos')
def update_todos(todo_ind: int, todo_update: dict):
    for todo in all_todos:
        if todo['todo_id'] == todo_ind:
            todo['todo_name'] = todo_update['todo_name']
            todo['todo_description'] = todo_update['todo_description']
            return todo
    return "Error, not found"

# Delete endpoint
@api.delete('/todos')
def delete_todos(todo_ind: int):
    for index, todo in enumerate(all_todos):
        if todo['todo_id'] == todo_ind:
            deleted_todo = all_todos.pop(index)
            return deleted_todo
    return "Error, not found"
            