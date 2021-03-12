from datetime import datetime, timedelta
from typing import Dict, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from db.crud import users
import db.models as models
import db.schemas as schemas
from db.session import get_db

from settings import ALGORITHM, DEFAULT_JWT_EXPIRE_MINS, SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# Login Handling
def verify_password(plain_text, hashed) -> bool:
    return pwd_context.verify(plain_text, hashed)


def hash_password(password) -> str:
    return pwd_context.hash(password)


def authenticate_user(db: Session, *, email: str, password: str) -> Optional[models.User]:
    user = users.get_one(db, email, get_password=True)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: Dict, expires_in: Optional[timedelta] = timedelta(days=DEFAULT_JWT_EXPIRE_MINS)) -> str:
    return jwt.encode({
        **data,
        'exp': datetime.utcnow() + expires_in
    }, SECRET_KEY, ALGORITHM)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> models.User:
    try:
        token_data = schemas.AuthPayload(**jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]))
        return users.get_one(db, email=token_data.email)
    except (JWTError, NoResultFound, ValidationError) as e:
        print(str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
