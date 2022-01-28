#fastapi hello world

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello_world():
    return {'message': 'Hello World'}

# Run the application
# $ uvicorn main:app --reload