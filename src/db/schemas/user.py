from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    is_active: Optional[bool]
    is_staff: Optional[bool]


# Properties required to create a new user
class UserCreate(UserBase):
    password: str


# Properties required to update an existing user
class UserUpdate(UserCreate):
    pass


# Properties of a user in the database for admin view
class UserData(UserBase):
    id: int
    last_login: Optional[datetime]
    date_joined: datetime

    class Config:
        orm_mode = True


class UserDataWithAuth(UserData):
    hashed_password: str


__all__ = ["UserBase", "UserCreate", "UserUpdate", "UserData", "UserDataWithAuth"]
