from fastapi import Request, Response
from fastapi.security.api_key import APIKeyHeader

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException


class APITokenMiddleware(BaseHTTPMiddleware):

    # Define API
    X_API_KEY = APIKeyHeader(name='X-API-Key')

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            key = await self.X_API_KEY(request)
        except HTTPException:
            return Response(status_code=403)

        response = await call_next(request)
        return response
