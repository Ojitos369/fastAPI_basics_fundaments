#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query

app = FastAPI()

# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get('/')
def hello_world():
    return {'message': 'Hello World'}

# Requests and Responses Body
@app.post('/person/new')
def create_person(person: Person = Body(...)): # '...' indicates that a parameter is obligatory
    return person

# Validaciones: Query params
@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(None, 
    min_length = 1, max_length = 50),
    age: str = Query(...)):
    # Mala practica que un query param sea obligatorio
    # Es recomenable que un path param si es obligatorio
    return {'name': name, 'age': age}



# max_length = max length of the string
# min_length = min length of the string
# regex = regular expression to validate the string
# ge = greater or equal than
# le = less or equal than
# gt = greater than
# lt = less than
# title = title of the parameter
# description = description of the parameter



# Run the application
# $ uvicorn main:app --reload