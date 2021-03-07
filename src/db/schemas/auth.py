from typing import Optional
from pydantic import BaseModel, EmailStr


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class AuthPayload(BaseModel):
    email: Optional[EmailStr] = None


__all__ = ['AuthToken', 'AuthPayload']
