from tokenize import String
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI()
my_posts =[{"title":"post 3", "content": "content of post 1", "id":1},
{"title":"post 4", "content": "content of post 2", "id":2}]
def find_post(id):
    for d in my_posts:
        if d['id'] == id:
            return d
#Schema using pydantic
class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int] = None

@app.get("/")
def root():
    return{"message":"Welcome to my api"}

@app.get("/posts")
def get_posts():
    return{"posts":my_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000000)
    my_posts.append(post_dict)
    return{"data": post}
#title str, content str, category, category

@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    post = find_post(id)
    print(post)
    return{"post_detail": post}