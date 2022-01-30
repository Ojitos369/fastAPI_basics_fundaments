import json
import requests

person = {
    "first_name": "John",
    "last_name": "Doe",
    "age": 25,
    "email": "john@doe.com",
    "hair_color": "brown",
    "is_married": True,
    "page": "https://john.doe.com"
}

location = {
    "city": "CDMX",
    "state": "CDMX",
    "country": "Mexico"
}

def hello_world_petition():
    answer = requests.get('http://localhost:8000')
    print(answer)
    answer = answer.json()
    print(answer)
    
def create_person_petition():
    answer = requests.post('http://localhost:8000/person/new', json = person)
    print(answer)
    answer = answer.json()
    print(answer)
    
def show_person_petition():
    print('Normal petition')
    answer = requests.get('http://localhost:8000/person/detail')
    print(answer)
    answer = answer.json()
    print(answer)
    print()
    print('With query params')
    answer = requests.get('http://localhost:8000/person/detail?age=25')
    print(answer)
    answer = answer.json()
    print(answer)
    print()
    print('With path params')
    answer = requests.get('http://localhost:8000/person/detail/21')
    print(answer)
    answer = answer.json()
    print(answer)
    
def update_person_petition():
    data = {
        "person": person,
        "location": location
    }
    answer = requests.put('http://localhost:8000/person/21', json = data)
    print(answer)
    answer = answer.json()
    print(answer)

if __name__ == '__main__':
    print('Hello World')
    hello_world_petition()
    print()
    print('-'*50)
    print()
    print('Create Person')
    create_person_petition()
    print()
    print('-'*50)
    print()
    print('Show Person')
    show_person_petition()
    print()
    print('-'*50)
    print()
    print('Update Person')
    update_person_petition()
    