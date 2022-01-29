#Python
from operator import eq
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field, HttpUrl, EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models
class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blond = 'blond'
    red = 'red'

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length = 1,
        max_length = 50
    )
    state: str = Field(
        ...,
        min_length = 1,
        max_length = 50
    )
    country: str = Field(
        ...,
        min_length = 1,
        max_length = 50
    )

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
    )
    last_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
    )
    age: int = Field(
        ...,
        gt = 0,
        le = 115
    )
    email: EmailStr = Field(
        ...
    )
    hair_color: Optional[HairColor] = Field(
        default = None
    )
    is_married: Optional[bool] = Field(
        default = None
    )
    page: Optional[HttpUrl] = Field(
        default = None
    )


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
    name: Optional[str] = Query(
        None,
        min_length = 1,
        max_length = 50,
        title = 'Person name',
        description = "This is de person name. It's between 1 and 50 characters long",
    ),
    age: str = Query(
        ...,
        title = 'Person age',
        description = 'This is the person age',
    )
):
    # Mala practica que un query param sea obligatorio
    # Es recomenable que un path param si es obligatorio
    return {'name': name, 'age': age}


# Validaciones: Path params
@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ...,
        gt = 0,
        title = 'Person id',
        description = 'This is the person id',
    )
):
    return {person_id: f'The person wiht {person_id} id exists'}


# Validaciones: Request Body
@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        gt = 0,
        title = 'Person id',
        description = 'This is the person id'
    ),
    person: Person = Body(
        ...,
        title = 'Person',
        description = 'This is the person'
    ),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results



# max_length = max length of the string
# min_length = min length of the string
# regex = regular expression to validate the string
# ge = greater or equal than
# le = less or equal than
# gt = greater than
# lt = less than
# title = title of the parameter
# description = description of the parameter


# Validaciones: Pydantic
# Clasicos:
#   str
#   int
#   float
#   bool
# Excoticos:
#   Enum
#   HttpUrl
#   FilePath
#   DirectoryPath
#   EmailStr
#   PaymentCardNumber
#   IPvAnyAddress
#   NegativeFloat
#   PositiveFloat
#   NegativeInt
#   PositiveInt

# Run the application
# $ uvicorn main:app --reload