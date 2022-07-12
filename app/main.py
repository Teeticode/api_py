
from fastapi import (Body, FastAPI,
 HTTPException, Response, status, Depends)
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas

from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()





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

#base of our api route
@app.get("/")
def root():
    return{"message":"Welcome to my api"}

#get all data from our model Posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()
    #print(posts)
    posts = db.query(models.Post).all()
    return{"posts":posts}
    

#add data to our model
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreateBase, db: Session = Depends(get_db)):
     
    post.postid = randrange(0, 20000000)
    #cursor.execute(""" INSERT INTO posts (title, content, published, postid)
     #                   values (%s, %s, %s, %s) RETURNING * """, (post.title, 
      #                  post.content, post.published, postid))
    #posts = cursor.fetchone()
    #conn.commit()
   
    posts = models.Post(**post.dict())
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts
#title str, content str, category, category

# get a specific post using the postid
@app.get("/posts/{postid}")
def get_post(postid: int, db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * from posts WHERE postid = %s """, (str(id),))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.postid == postid).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {postid} was not found")
        
    return post

# delete route
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    #find index in array that has required ID
    #my_posts.pop
    #cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.postid == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update route
@app.put('/posts/{id}', response_model=schemas.PostUpdate)
def update_post(id: int, post:schemas.UpdateBase, db: Session = Depends(get_db)):
    #cursor.execute(""" UPDATE posts SET title=%s, content = %s, published = %s WHERE postid=%s RETURNING *""", 
     #               (post.title, post.content, post.published, str(id),))
    #updated_post = cursor.fetchone()
    #conn.commit()vb
   
    post_query = db.query(models.Post).filter(models.Post.postid == id)
    if post_query.first() == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post with id: {id} does not exist")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()
