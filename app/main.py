from fastapi import (Body, FastAPI,
 HTTPException, Response, status, Depends)
from random import randrange
from typing import List
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

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



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
#base of our api route
@app.get("/")
def root():
    return{"message":"Welcome to my api"}

