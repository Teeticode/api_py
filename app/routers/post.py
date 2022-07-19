from email.policy import HTTP
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from fastapi import ( APIRouter,
 HTTPException, Response, status, Depends)
from random import randrange
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
#get all data from our model Posts
@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    limit: int=10,
    search: Optional[str] =""
):
    #cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()
    #print(posts)

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()

    return posts
    
# get all projects of collaborator 
@router.get('/colab', response_model=List[schemas.Post])
def get_colab_posts(db: Session = Depends(get_db),
                    curr_user: int=Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.userid == curr_user.userid).all()
    return posts
#add data to our model
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
        post: schemas.CreateBase, 
        db: Session = Depends(get_db), 
        curr_user: int = Depends(oauth2.get_current_user)):
    post.postid = randrange(0, 20000000)
    post.userid = curr_user.userid
    #cursor.execute(""" INSERT INTO posts (title, content, published, postid)
     #                   values (%s, %s, %s, %s) RETURNING * """, (post.title, 
      #                  post.content, post.published, postid))
    #posts = cursor.fetchone()
    #conn.commit()
    print(curr_user.email) 
    posts = models.Post(**post.dict())
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts
#title str, content str, category, category

# get a specific post using the postid
@router.get("/{postid}", response_model=schemas.Post)
def get_post(
    postid: int, 
    db: Session = Depends(get_db),
    curr_user : int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * from posts WHERE postid = %s """, (str(id),))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.postid == postid).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {postid} was not found")
    
    if post.userid != curr_user.userid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Could not get post")
    return post


# delete route
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db),
    curr_user: int=Depends(oauth2.get_current_user)
    ):
    #find index in array that has required ID
    #my_posts.pop
    #cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.postid == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} does not exist")
    
    if post_query.first().userid != curr_user.userid:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                           detail="Not authorized to perform action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update route
@router.put('/{postid}', response_model=schemas.PostUpdate)
def update_post(
    postid: int, 
    post:schemas.UpdateBase, 
    db: Session = Depends(get_db),
    curr_user: int= Depends(oauth2.get_current_user)
    ):
    #cursor.execute(""" UPDATE posts SET title=%s, content = %s, published = %s WHERE postid=%s RETURNING *""", 
     #               (post.title, post.content, post.published, str(id),))
    #updated_post = cursor.fetchone()
    #conn.commit()vb
   
    post_query = db.query(models.Post).filter(models.Post.postid == postid)
    if post_query.first() == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {postid} does not exist")
    
    if post_query.first().userid != curr_user.userid:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                           detail="Not authorized to perform action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()


