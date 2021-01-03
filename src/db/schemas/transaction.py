from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel

from .connector import Connector
from .token import Token


# Transactions have no CRUD models - read only
class TransactionBase(BaseModel):
    id: int
    start_timestamp: datetime
    end_timestamp: datetime
    duration: timedelta
    meter_start: int
    meter_stop: int
    meter_used: int


# Data model doesn't contain information about charger/connector etc
class TransactionData(TransactionBase):

    class Config:
        orm_mode = True


# Transaction model has information about the connector
class Transaction(TransactionBase):
    id: int
    reservation_id: Optional[int]
    connector: Connector
    end_token: Optional[Token]
    start_token: Optional[Token]
    stop_reason: Optional[str]

    class Config:
        orm_mode = True


__all__ = ['TransactionBase', 'TransactionData', 'Transaction']
