from tokenize import String
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
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

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000000)
    my_posts.append(post_dict)
    return{"data": post}
#title str, content str, category, category
@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return{"data": post}

@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
        
    print(post)
    return{"post_detail": post}

