from fastapi.websockets import WebSocket as FastAPIWebsocket
from starlette.websockets import WebSocket as StarletteWebSocket


class StarletteWebSocketAdaptor(object):

    def __init__(self, websocket: StarletteWebSocket):
        self._websocket = websocket

    async def recv(self):
            return await self._websocket.receive_text()

    async def send(self, message: str):
        await self._websocket.send_text(message)

    async def close(self, code: int, reason: str) -> None:
        await self._websocket.close(code)

    @property
    def request_headers(self):
        return self._websocket.headers

    @property
    def subprotocol(self):
        return 'ocpp1.6'


class FastAPIWebSocketAdaptor(object):

    def __init__(self, websocket: FastAPIWebsocket):
        self._websocket = websocket

    async def recv(self):
            return await self._websocket.receive_text()

    async def send(self, message: str):
        await self._websocket.send_text(message)

    async def close(self, code: int, reason: str) -> None:
        await self._websocket.close(code)

    @property
    def request_headers(self):
        return self._websocket.headers

    @property
    def subprotocol(self):
        return 'ocpp1.6'
