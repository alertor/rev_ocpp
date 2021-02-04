from fastapi import FastAPI

from central_system.log_router import router as log_router
from central_system.router import router as cs_router
from central_system.websocket_router import router as ocpp_router
from data_api.router import router as data_api_router


app = FastAPI()

# Data access endpoint
app.include_router(
    data_api_router,
    prefix='/api'
)

app.include_router(
    log_router,
    prefix='/cs/logs'
)

# Control router
app.include_router(
    cs_router,
    prefix='/cs'
)

# Websocket endpoint for charge points
app.include_router(
    ocpp_router,
    prefix='/ocpp/1_6')


