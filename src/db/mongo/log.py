import os
import pymongo

from typing import Optional

from bson.codec_options import CodecOptions

import settings

# Initialise DB connection
client = pymongo.MongoClient(
    settings.MONGO_ADDR,
    username=settings.MONGO_USER,
    password=settings.MONGO_PASS,
    serverSelectionTimeoutMS=1000
)

db = client['ocpp'].with_options(codec_options=CodecOptions(
    tz_aware=True
))


def log_message(message, path: Optional[str] = None):
    col = db[path if path else 'ocpp_msgs']
    col.insert_one(message)


__all__ = ['log_message']
