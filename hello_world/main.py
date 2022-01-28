#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body

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

# Run the application
# $ uvicorn main:app --reload