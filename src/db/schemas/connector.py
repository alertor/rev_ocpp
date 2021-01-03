from pydantic import BaseModel

from .chargepoint import ChargePoint


class ConnectorBase(BaseModel):
    connector_id: int
    chargepoint: ChargePoint


# Read class
class Connector(ConnectorBase):
    id: int
    available: bool
    in_use: bool

    class Config:
        orm_mode = True


__all__ = ["ConnectorBase", "Connector"]
