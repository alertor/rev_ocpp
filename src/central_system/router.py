from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect

from db.session import session
from network.websocket_adaptor import FastAPIWebSocketAdaptor

from chargepoint import VeefillChargePoint
from chargepoint.exceptions import ChargePointNotAuthorized

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


async def _handle_request(websocket: FastAPIWebSocketAdaptor, path):
    """ For every new charge point that connects, create a ChargePoint
    instance and start listening for messages.
    """
    # Extract the ID from the request path
    charge_point_id = path.strip('/')

    with session() as s:
        try:
            cp = VeefillChargePoint(charge_point_id, websocket, s)
            await cp.start()
        except WebSocketDisconnect as e:
            print(str(e))
        except ChargePointNotAuthorized:
            print('Charge point not authorized')


@router.websocket("/{point_id}")
async def connect_chargepoint(websocket: WebSocket, point_id: str) -> None:
    await websocket.accept(subprotocol='ocpp1.6')
    _websocket_adaptor = FastAPIWebSocketAdaptor(websocket)
    await _handle_request(_websocket_adaptor, point_id)

