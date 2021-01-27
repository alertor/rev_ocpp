from datetime import datetime

from pydantic import BaseModel


class UsageBase(BaseModel):
    bucket_start: datetime


class UsageCount(UsageBase):
    count: int


class UsageKWH(BaseModel):
    kwh: int


class Usage(UsageCount, UsageKWH):
    pass


__all__ = ['UsageCount', 'UsageKWH', 'Usage']
