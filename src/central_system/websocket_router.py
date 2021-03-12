from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect

from db.mongo.log import log_connect
from db.session import session
from network.websocket_adaptor import StarletteWebSocketAdaptor

from chargepoint import VeefillChargePoint
from chargepoint.exceptions import ChargePointNotAuthorized

from .auth import authenticate_charge_point
from . import central_system

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


async def _handle_request(websocket: StarletteWebSocketAdaptor, path):
    """ For every new charge point that connects, create a ChargePoint
    instance and start listening for messages.
    """
    # Extract the ID from the request path
    charge_point_id = path.strip('/')

    with session() as s:
        try:
            cp = VeefillChargePoint(charge_point_id, websocket, s)
            central_system.register_chargepoint(cp)
            await cp.start()
        except WebSocketDisconnect as e:
            print(str(e))
        except ChargePointNotAuthorized:
            print('Charge point not authorized')
        finally:
            central_system.deregister_chargepoint(cp)


@router.websocket("/{point_id}")
async def connect_chargepoint(websocket: WebSocket, point_id: str) -> None:
    # Log the connection attempt for debug
    log_connect(point_id)

    # Authenticate charge point
    # OCPP spec requires rejection of the HTTP request if id is invalid
    # Closing the socket before accepting returns a 403
    if not authenticate_charge_point(point_id):
        return await websocket.close(code=1008)

    # Accept and check protocol is correct
    await websocket.accept(subprotocol='ocpp1.6')
    if websocket.headers['Sec-WebSocket-Protocol'] != 'ocpp1.6':
        await websocket.close()

    # Apply the FastAPI (Starlette) websocket adaptor since ocpp library wants .recv and .send
    _websocket_adaptor = StarletteWebSocketAdaptor(websocket)
    await _handle_request(_websocket_adaptor, point_id)
    await websocket.close()
