from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils
router = APIRouter(
    tags=['Authentication'],
    prefix="/auth"
)

@router.post('/login')
def login(user_cr: schemas.UserLogin, db: Session=Depends(database.get_db)):
    log_user = db.query(models.User).filter(models.User.email == user_cr.email).first()
    if not log_user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')
    if not utils.verify_psd(user_cr.password, log_user.password):
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')

    # create a token
    # return token
    return{'token':log_user}
