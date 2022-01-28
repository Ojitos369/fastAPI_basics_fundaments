#fastapi hello world

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello_world():
    return {'message': 'Hello World'}

@app.get('/tweets/{tweet_id}')
def get_tweet(tweet_id='unknown_id_value'):
    data = {
        "tweet_id": tweet_id,
        "content": f"This is data from tweet {tweet_id}"
    }
    return data

@app.put('/user/{user_id}/details?name=no_dado&age=no_dado')
def user_data(user_id, name='no_dado', age='no_dado'):
    data = {
        "user_id": user_id
    }
    if name != 'no_dado':
        data["name"] = name
    if age != 'no_dado':
        data["age"] = age
    return data

# Run the application
# $ uvicorn main:app --reload