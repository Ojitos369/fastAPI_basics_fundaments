#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field, HttpUrl, EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File

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
    status_code = status.HTTP_200_OK,
    tags = ["Pages", "Home"]
)
def hello_world():
    """Hello World
    The first endpoint of the API.
    Requests Example:
    - **requests.get('localhost:8000/')**
    
    Returns:
    - A json objet with a hello world message.
    
    """
    return {'message': 'Hello World'}
    


# Requests and Responses Body
@app.post(path = '/person/new',
    response_model = PersonOut,
    status_code = status.HTTP_201_CREATED,
    tags = ["Persons"],
    summary = "Create person in the app",
)
def create_person(person: Person = Body(...)): # '...' indicates that a parameter is obligatory
    """Create Person
    
    This path operation creates a person in the app and save the information in the database.
    
    Requests Example:
     - **requests.post('localhost:8000/person/new', json = global person)**
    
    Parameters:
    - Request body parameters:
        - **person: Person** -> A person model with first name, last name, age, email, password, hair color, marital status and page.
    
    Returns a person model with first name, last name, age, email, hair color, marital status and page.
    """
    return person


# Validaciones: Query params
@app.get(path = '/person/detail',
    status_code = status.HTTP_200_OK,
    tags = ["Persons"],
    summary = "Show Same Persons",
    deprecated = True
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
    """Show Same Persons
    Show a listo of persons with the same name and age.
    
    Requests Example:
    - **requests.get('localhost:8000/person/detail?name=John&age=25')**

    Args:
    - Query parameters:
        - Required:
            - **age: int** -> The person age.
        - Optional:
            - **name: str** -> The person name.

    Returns:
    - A json with the list of persons with the same name and age.
    """
    # Mala practica que un query param sea obligatorio
    # Es recomenable que un path param si es obligatorio
    return {"results": [{'name': name, 'age': age}]}
    


persons_id = [1, 2, 3, 4, 5]

# Validaciones: Path params
@app.get(path = '/person/detail/{person_id}',
    status_code = status.HTTP_200_OK,
    tags = ["Persons"],
    summary = "Show person exisiting in the app",
)
def show_person(
    person_id: int = Path(
        ...,
        gt = 0,
        title = 'Person id',
        description = 'This is the person id',
        example = 3
    )
):
    """Show Person
    Get the info about a person existing in the app.
    Requests Example:
    - **requests.get('http://localhost:8000/person/detail/1')**
    
    Args:
    - Path parameters:
        - **person_id: int** -> The person id.
    
    Returns:
        - Json with the person id
        
    Raises:
        - HTTPException: 404 -> If the person id is not found.
    """
    if person_id not in persons_id:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Person not found'
        )
    else:
        return {person_id: f'The person wiht {person_id} id exists'}
    


# Validaciones: Request Body
@app.put(path = '/person/{person_id}',
    status_code = status.HTTP_200_OK,
    tags = ["Persons"],
    summary = "Update person's info",
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
    """Update Person
    
    Update the info about a person existing in the app.
    Requests Example:
    - **requests.put(f'http://localhost:8000/person/{person_id}', json = global person)**
    
    Args:
    - Path parameters:
        - **person_id: int** -> The person id.
    - Request body parameters:
        - **person: Person** -> A person model with first name, last name, age, email, password, hair color, marital status and page.
        - **location: Location** -> A location model with city, state and country.
    
    Returns:
    - Dictionary with the person and location updated.
    
    Raises:
    - HTTPException: 404 -> If the person id is not found.
    """
    if person_id not in persons_id:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Person not found'
        )
    else:
        results = person.dict()
        results.update(location.dict())
        return results


# Forms
@app.post(path = '/login',
    response_model = LoginOut,
    status_code = status.HTTP_200_OK,
    tags = ["Persons", "Pages"],
    summary = 'User login'
)
def login(
    username: str = Form(
        ...
    ),
    password: str = Form(
        ...
    )
    
):
    """Login
    Authenticate a user in the app.
    
    Args:
    - Form parameters:
        - **username: str** -> The user name.
        - **password: str** -> The user password.
        
    Returns:
    - a LoginOut model with the username.
    """
    return LoginOut(username = username)


# Cookies and Headers Params
@app.post(path = '/contact',
    status_code = status.HTTP_200_OK,
    tags = ["Pages", "Contact"],
    summary = 'Contact form'
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
    """Contact
    Contact with the app's owner.
    
    Args:
    - Form parameters:
        - **first_name: str** -> The user first name.
        - **last_name: str** -> The user last name.
        - **email: EmailStr** -> The user email.
    - Header parameters:
        - **user_agent: str** -> The user agent.
    - Cookie parameters:
        - **ads: str** -> The cookies from de user.
        
    Returns:
    - User Agent's info.
    """
    return user_agent


# Files
@app.post(path = '/post-image',
    status_code = status.HTTP_200_OK,
    tags = ["Pages", "Files"],
    summary = 'Image upload'
)
def post_image(
    image: UploadFile = File(...)
):
    """Post Image
    Send a image to the app.
    
    Args:
    - File parameters:
        - **image: UploadFile** -> The image to send.
        
    Returns:
    - A json with the image info. name, type and size in kb.
    
    """
    file = {
        "filename": image.filename,
        "format": image.content_type,
        "size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }
    # save file
    with open(f'./files/{image.filename}', 'wb') as f:
        f.write(image.file.read())
    return file

"""
max_length = max length of the string
min_length = min length of the string
regex = regular expression to validate the string
ge = greater or equal than
le = less or equal than
gt = greater than
lt = less than
title = title of the parameter
description = description of the parameter
"""

"""
Validaciones: Pydantic
Clasicos:
  str
  int
  float
  bool
Excoticos:
  Enum
  HttpUrl
  FilePath
  DirectoryPath
  EmailStr
  PaymentCardNumber
  IPvAnyAddress
  NegativeFloat
  PositiveFloat
  NegativeInt
  PositiveInt
"""


"""
Files
* File
* UploadFile
    -> filename
    -> content_type (jpg, mp4, gif, etc)
    -> file
"""

# Run the application
# $ uvicorn main:app --reload


# Deprecar <- Depricate = Descontinuado