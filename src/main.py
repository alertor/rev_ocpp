from fastapi import FastAPI

from central_system.router import router as central_system_router
from data_api.router import router as data_api_router
from middleware.security import APITokenMiddleware


api = FastAPI()
ocpp = FastAPI()


# api.add_middleware(APITokenMiddleware)


# Data access endpoint
api.include_router(
    data_api_router,
    prefix='/api'
)


# Websocket endpoint for charge points
ocpp.include_router(
    central_system_router,
    prefix='/ocpp/1_6')


