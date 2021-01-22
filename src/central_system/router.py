from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from ocpp.v16 import call

from . import central_system

router = APIRouter(
    responses={404: {"description": "Not found"}}
)


@router.get("/list")
async def list_connected_points():
    return central_system.chargepoints


# Config API
@router.get("/{point_id}/mode")
async def get_point_free(point_id: str):
    try:
        cp = central_system.get_chargepoint(point_id)
        request = call.GetConfigurationPayload(
            key=['HU1.CCURFIDDisable']
        )   
        response = await cp.call(request)
        print(response)
        return response
    except KeyError:
        print(f'No chargepoint with id {point_id}')
        return HTTPException(status_code=404)
