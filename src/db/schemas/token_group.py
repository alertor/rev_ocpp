from pydantic import BaseModel


class TokenGroupBase(BaseModel):
    token: str


class TokenGroup(TokenGroupBase):

    class Config:
        orm_mode = True


class TokenGroupCreate(TokenGroupBase):
    pass


__all__ = ['TokenGroupBase', 'TokenGroup', 'TokenGroupCreate']
