from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    responses={404: {"description": "Not found"}}
)


@router.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

__all__ = ['router']
