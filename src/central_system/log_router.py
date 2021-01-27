from typing import Dict, List, Optional

from fastapi import APIRouter, Query

from ocpp.v16.enums import Action

from db.mongo.log import get_connection_log, get_message_log
from util import parse_iso_parameter

router = APIRouter(
    responses={404: {"description": "Not found"}}
)


@router.get('/connections', response_model=List[Dict])
async def get_connection_log_items(
        from_time: Optional[str] = Query(None, alias='from'),
        to_time: Optional[str] = Query(None, alias='to'),
):
    _from = parse_iso_parameter(from_time)
    _to = parse_iso_parameter(to_time)
    return get_connection_log(_from, _to)


@router.get('/{chargepoint_id}', response_model=List[Dict])
async def get_message_log_items(
        chargepoint_id: str,
        action: Optional[List[Action]] = Query(None),
        from_time: Optional[str] = Query(None, alias='from'),
        to_time: Optional[str] = Query(None, alias='to'),
):
    _from = parse_iso_parameter(from_time)
    _to = parse_iso_parameter(to_time)
    return get_message_log(chargepoint_id, action, _from, _to)
