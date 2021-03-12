import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.crud import users
import db.models as models
import db.schemas as schemas
from db.session import get_db

from .auth import authenticate_user, create_access_token, get_current_user


router = APIRouter(
    responses={404: {"description": "Not found"}}
)


@router.post("/auth", response_model=schemas.AuthResponse)
async def login_auth_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    time.sleep(1)
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if user is None:
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    elif not user.is_active:
        raise HTTPException(status_code=400, detail='Invalid user')

    return {
        'access_token': create_access_token({'email': user.email}),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'token_type': 'bearer'
    }


@router.get('/me')
async def get_me(current_user: models.User = Depends(get_current_user)):
    return {
        current_user.first_name,
        current_user.last_name,
        current_user.email
    }


@router.post('/signup', response_model=schemas.UserBase)
async def create_user(*, db: Session = Depends(get_db), new_user: schemas.UserCreate):
    user = users.get_one(db=db, email=new_user.email)
    if user:
        raise HTTPException(status_code=400, detail='A user with this email already exists')

    user = users.create(db, user=new_user)
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }

__all__ = ['router']
