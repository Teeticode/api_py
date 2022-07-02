from tokenize import String
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()
my_posts =[{"title":"post 3", "content": "content of post 1", "id":1},
{"title":"post 4", "content": "content of post 2", "id":2}]
def find_post(id):
    for d in my_posts:
        if d['id'] == id:
            return d

while True:
    try: 
        conn = psycopg2.connect(host='localhost',database='portfolio', user='postgres',
        password='dennis', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print("Connecting to a database was not successfull")
        print("Error: ", error)
        time.sleep(2)
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i
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

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #find index in array that has required ID
    #my_posts.pop
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post:Post):
    print(post)
    index = find_index_post(id)

    if index == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post with id: {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts['index'] = post_dict
    return {'message': post_dict}