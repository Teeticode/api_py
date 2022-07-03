from tokenize import String
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from requests import post

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
    postid: Optional[int]

@app.get("/")
def root():
    return{"message":"Welcome to my api"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return{"posts":posts}
    
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    postid = post.postid 
    postid = randrange(0, 20000000)
    cursor.execute(""" INSERT INTO posts (title, content, published, postid)
                        values (%s, %s, %s, %s) RETURNING * """, (post.title, 
                        post.content, post.published, postid))
    posts = cursor.fetchone()
    conn.commit()
    return{"data": posts}
#title str, content str, category, category
@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return{"data": post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * from posts WHERE postid = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
        
    return{"post_detail": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #find index in array that has required ID
    #my_posts.pop
    cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT, detail=deleted_post)


@app.put('/posts/{id}')
def update_post(id: int, post:Post):
    cursor.execute(""" UPDATE posts SET title=%s, content = %s, published = %s WHERE postid=%s RETURNING *""", 
                    (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post with id: {id} does not exist")
    return {'message': updated_post}
