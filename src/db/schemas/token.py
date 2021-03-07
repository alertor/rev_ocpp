from typing import Optional

from pydantic import BaseModel

from .token_group import TokenGroup


class TokenBase(BaseModel):
    token: str
    token_group: Optional[TokenGroup]


class Token(TokenBase):

    class Config:
        orm_mode = True


class TokenCreate(TokenBase):
    pass


__all__ = ['TokenBase', 'TokenCreate', 'Token']
