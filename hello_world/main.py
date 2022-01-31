#Python
from lib2to3.pgen2.token import OP
from operator import eq
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field, HttpUrl, EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path, Form, Header, Cookie

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

    class Config:
        schema_extra = {
            "example": {
                "city": "CDMX",
                "state": "CDMX",
                "country": "Mexico"
            }
        }

class BasePerson(BaseModel):
    first_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example = 'John'
    )
    last_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example = 'Doe'
    )
    age: int = Field(
        ...,
        gt = 0,
        le = 115,
        example = 25
    )
    email: EmailStr = Field(
        ...,
        example = "john@doe.com"
    )
    hair_color: Optional[HairColor] = Field(
        default = None,
        example = HairColor.brown
    )
    is_married: Optional[bool] = Field(
        default = None,
        example = True
    )
    page: Optional[HttpUrl] = Field(
        default = None,
        example = "https://john.doe.com"
    )
    
    """ class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "age": 25,
                "email": "john@doe.com",
                "hair_color": HairColor.brown,
                "is_married": True,
                "page": "https://www.john.doe.com"
            }
        } """


class Person(BasePerson):
    password: str = Field(
        ...,
        min_length = 8,
        example = "12345678"
    )
    
class PersonOut(BasePerson):
    pass

class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length = 20,
        example = 'ojitos369'
    )
    message: str = Field(
        default = 'Login successful'
    )


# Person Example
"""
person = {
    "first_name": "John",
    "last_name": "Doe",
    "age": 25,
    "email": "john@doe.com",
    "hair_color": HairColor.brown,
    "is_married": True,
    "page": "https://www.john.doe.com"
}
"""

@app.get(path = '/',
    status_code = status.HTTP_200_OK
)
def hello_world():
    return {'message': 'Hello World'}
    # Requests Example
    # requests.get('localhost:8000/')


# Requests and Responses Body
@app.post(path = '/person/new',
    response_model = PersonOut,
    status_code = status.HTTP_201_CREATED
)
def create_person(person: Person = Body(...)): # '...' indicates that a parameter is obligatory
    return person
    # Requests Example
    # requests.post('localhost:8000/person/new', json = global person)


# Validaciones: Query params
@app.get(path = '/person/detail',
    status_code = status.HTTP_200_OK
)
def show_person(
    name: Optional[str] = Query(
        None,
        min_length = 1,
        max_length = 50,
        title = 'Person name',
        description = "This is de person name. It's between 1 and 50 characters long",
        example = 'John Doe'
    ),
    age: int = Query(
        ...,
        title = 'Person age',
        description = 'This is the person age',
        example = 25
    )
):
    # Mala practica que un query param sea obligatorio
    # Es recomenable que un path param si es obligatorio
    return {'name': name, 'age': age}
    # Requests Example
    # requests.get('localhost:8000/person/detail?name=John&age=25')


# Validaciones: Path params
@app.get(path = '/person/detail/{person_id}',
    status_code = status.HTTP_200_OK
)
def show_person(
    person_id: int = Path(
        ...,
        gt = 0,
        title = 'Person id',
        description = 'This is the person id',
        example = 21
    )
):
    return {person_id: f'The person wiht {person_id} id exists'}
    # Requests Example
    # requests.get('http://localhost:8000/person/detail/1')


# Validaciones: Request Body
@app.put(path = '/person/{person_id}',
    status_code = status.HTTP_200_OK
)
def update_person(
    person_id: int = Path(
        ...,
        gt = 0,
        title = 'Person id',
        description = 'This is the person id',
        example = 21
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
    # Requests Example
    # requests.put(f'http://localhost:8000/person/{person_id}', json = global person)


# Forms
@app.post(path = '/login',
    response_model = LoginOut,
    status_code = status.HTTP_200_OK
)
def login(
    username: str = Form(
        ...
    ),
    password: str = Form(
        ...
    )
    
):
    return LoginOut(username = username)


# Cookies and Headers Params
@app.post(path = '/contact',
    status_code = status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length = 20,
        min_length = 1
    ),
    last_name: str = Form(
        ...,
        max_length = 20,
        min_length = 1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length = 20,
        example = "aqui va un mensaje de al menos 20 caracteres"
    ),
    user_agent: Optional[str] = Header(default = None),
    ads: Optional[str] = Cookie(default = None)
):
    return user_agent





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
