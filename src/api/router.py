from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.crud import get_transactions
from db.session import get_db
from db import schemas
from util import parse_iso_parameter

from .aggregation import get_usage

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


@router.get('/usage', response_model=List)
async def get_usage_items(
        db: Session = Depends(get_db),
        chargepoint: Optional[str] = None,
        from_time: Optional[str] = Query(None, alias='from'),
        to_time: Optional[str] = Query(None, alias='to'),
        named: Optional[bool] = False,
        header: Optional[bool] = False
):
    _from = parse_iso_parameter(from_time)
    _to = parse_iso_parameter(to_time)
    result = get_usage(db, chargepoint=chargepoint, from_timestamp=_from, to_timestamp=_to)
    if header:
        return [['Date', 'Count', 'kWh']] + result
    elif named:
        return [r._asdict() for r in result] if named else result
    return result


@router.get('/usage/kwh', response_model=List)
async def get_usage_kwh_items(
        db: Session = Depends(get_db),
        chargepoint: Optional[str] = None,
        from_time: Optional[str] = Query(None, alias='from'),
        to_time: Optional[str] = Query(None, alias='to'),
        named: Optional[bool] = False,
        header: Optional[bool] = False
):
    _from = parse_iso_parameter(from_time)
    _to = parse_iso_parameter(to_time)
    result = get_usage(db, kwh=True, count=False, chargepoint=chargepoint, from_timestamp=_from, to_timestamp=_to)
    if header:
        return [['Date', 'kWh']] + result
    elif named:
        return [r._asdict() for r in result] if named else result
    return result


@router.get('/usage/count', response_model=List)
async def get_usage_count_items(
        db: Session = Depends(get_db),
        chargepoint: Optional[str] = None,
        from_time: Optional[str] = Query(None, alias='from'),
        to_time: Optional[str] = Query(None, alias='to'),
        named: Optional[bool] = False,
        header: Optional[bool] = False
):
    _from = parse_iso_parameter(from_time)
    _to = parse_iso_parameter(to_time)
    result = get_usage(db, kwh=False, count=True, chargepoint=chargepoint, from_timestamp=_from, to_timestamp=_to)
    if header:
        return [['Date', 'Count']] + result
    elif named:
        return [r._asdict() for r in result] if named else result
    return result
