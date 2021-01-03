from fastapi import FastAPI

from starlette.endpoints import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from central_system.router import router as central_system_router
from data_api.router import router as data_api_router

app = FastAPI()


# Websocket endpoint for charge points
app.include_router(
    central_system_router,
    prefix='/ocpp/1_6')


# Data access endpoint
app.include_router(
    data_api_router,
    prefix='/data'
)
