from typing import Optional
from pydantic import BaseModel, EmailStr

from .user import UserBase


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class AuthPayload(BaseModel):
    email: Optional[EmailStr] = None


class AuthResponse(AuthToken, UserBase):
    pass


__all__ = ['AuthToken', 'AuthPayload', 'AuthResponse']
