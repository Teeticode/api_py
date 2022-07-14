from http.client import HTTPException
from wsgiref import headers
from fastapi import Depends, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = "yellodonnoQhgCpn9KQKhq.aZeuPlFDRCXyPlIhBuLhfocWHQenvN2uEO"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        userid : str = payload.get("user_id")
        if userid is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=userid)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Cannot validate credintials",
            headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)