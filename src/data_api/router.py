from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.crud import get_transactions_by_datetime
from db.session import get_db
from db import schemas
from util import parse_iso_parameter


router = APIRouter(
    responses={404: {"description": "Not found"}}
)


@router.get('/transactions/', response_model=List[schemas.TransactionData])
async def get_transactions(
        db: Session = Depends(get_db),
        from_time: Optional[str] = Query(None, alias='from'),
        to_time: Optional[str] = Query(None, alias='to')
):
    _from = parse_iso_parameter(from_time)
    _to = parse_iso_parameter(to_time)
    return get_transactions_by_datetime(db, _from, _to)
