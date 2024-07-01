from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
async def root():
    return {"message" : "Hello World"}



class Post(BaseModel):
    post_id : int
    title : str
    content : str
    
temp_database : Post = []

@app.post('/post')
async def create_post(req : Post):
    temp_database.append(req)
    return {
        "response" : "success",
        "posts" : temp_database
    }

app.put('/post')
async def update_post(req : Post, post_id : int):
    for i in temp_database:
        if post_id == i.post_id
