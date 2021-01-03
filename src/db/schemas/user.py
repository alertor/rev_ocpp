from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str


class User(BaseModel):
    id: int
    last_login: Optional[datetime]
    date_joined: datetime

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


__all__ = ["UserBase", "UserCreate", "User"]
