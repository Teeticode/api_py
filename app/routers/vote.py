from fastapi import (APIRouter, Response, status, HTTPException, Depends)
from .. import database, models, utils, oauth2,schemas 
from sqlalchemy.orm import Session
router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,
        curr_user: int= Depends(oauth2.get_current_user),
        db: Session=Depends(database.get_db)):
    
    post = db.query(models.Post).filter(models.Post.postid == vote.postid).first()

    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Post with id {vote.postid} not found')

    vote_query = db.query(models.Vote).filter(models.Vote.postid == vote.postid, 
        models.Vote.userid == curr_user.userid)
    found_vote = vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=f'user {curr_user.userid} has already voted on post')
        new_vote = models.Vote(postid = vote.postid, userid = curr_user.userid)
        db.add(new_vote)
        db.commit()
        return {'message': 'successfully added vote'}
    elif(vote.dir == 0):
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Vote not found')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message':'successfully deleted vote'}

@router.get('/')
def get_votes(
    db: Session = Depends(database.get_db),
):
    votes = db.query(models.Vote).all()
    return votes
