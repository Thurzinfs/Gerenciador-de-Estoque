from pwdlib import PasswordHash
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import jwt

from jwt.exceptions import PyJWTError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.db.database import get_session
from fastapi import Depends
from app.models.model_user import User
from fastapi import HTTPException
from http import HTTPStatus
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITMO = settings.ALGORITHM
ACESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_acess_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({
        'exp' : expire
    })
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITMO)
    return encode_jwt 

def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme)
):
    CREDENTIALS_EXCEPTION = HTTPException(
        status_code = HTTPStatus.UNAUTHORIZED,
        detail = 'Could not validate credentials',
        headers={"WWW-Authenticate" : 'Bearer'}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])
        email: str = payload.get('sub')

        if email is None:
            raise CREDENTIALS_EXCEPTION
        
    except PyJWTError as e:
        raise CREDENTIALS_EXCEPTION

    db = session.query(User).filter(User.email == email).first()
    if not db:
        raise CREDENTIALS_EXCEPTION
    return db
