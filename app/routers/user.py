from fastapi import (APIRouter,
 HTTPException, status, Depends)
from random import randrange
from typing import List

from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)
# Create user
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.userid = randrange(0, 50000000)
    # hash the password
    hashed_psd = utils.hash(user.password)
    user.password = hashed_psd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# get all users

@router.get('/', response_model=List[schemas.UserOut])
def get_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# get individual user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.userid == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    return user