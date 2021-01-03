from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChargePointBase(BaseModel):
    model: str
    vendor: str
    serial_number: Optional[str]
    firmware: Optional[str]
    type: str
    identity: str


# Read class
class ChargePoint(ChargePointBase):
    id: int
    last_heartbeat: Optional[datetime]
    boot_timestamp: Optional[datetime]
    connected: bool

    class Config:
        orm_mode = True


__all__ = ["ChargePointBase", "ChargePoint"]
