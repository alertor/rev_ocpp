from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ocpp.v16.enums import Action

from db.crud import get_transactions
from db.mongo.log import get_connection_log, get_message_log
from db.session import get_db
from db import schemas
from util import parse_iso_parameter


router = APIRouter(
    responses={404: {"description": "Not found"}}
)


@router.get('/transactions/', response_model=List[schemas.TransactionData])
async def get_transaction_items(
        db: Session = Depends(get_db),
        from_time: Optional[str] = Query(None, alias='from'),
        to_time: Optional[str] = Query(None, alias='to'),
        over: Optional[int] = Query(None)
):
    _from = parse_iso_parameter(from_time)
    _to = parse_iso_parameter(to_time)
    return get_transactions(db, from_timestamp=_from, to_timestamp=_to, meter_over=over)


@router.get('/logs/connections', response_model=List[Dict])
async def get_connection_log_items(
        from_time: Optional[str] = Query(None, alias='from'),
        to_time: Optional[str] = Query(None, alias='to'),
):
    _from = parse_iso_parameter(from_time)
    _to = parse_iso_parameter(to_time)
    return get_connection_log(_from, _to)


@router.get('/logs/{chargepoint_id}', response_model=List[Dict])
async def get_message_log_items(
        chargepoint_id: str,
        action: Optional[List[Action]] = Query(None),
        from_time: Optional[str] = Query(None, alias='from'),
        to_time: Optional[str] = Query(None, alias='to'),
):
    _from = parse_iso_parameter(from_time)
    _to = parse_iso_parameter(to_time)
    return get_message_log(chargepoint_id, action, _from, _to)
