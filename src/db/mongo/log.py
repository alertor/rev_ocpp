from bson.codec_options import CodecOptions
from datetime import datetime
import pymongo
from typing import Dict, List, Optional

from ocpp.v16.enums import Action

import settings
from util import utc_datetime

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


# Convert 'ObjectID' from Mongo into string id
def _modify_id(data: List[Dict]) -> List:
    for x in data:
        try:
            x['id'] = str(x.pop('_id'))
        except KeyError:
            pass
    return data


def log_message(message, path: Optional[str] = None):
    col = db[path if path else 'ocpp_msgs']
    col.insert_one({
        **message,
        'timestamp': utc_datetime()
    })


def get_log(
        path: str,
        action: Optional[Action] = None,
        from_timestamp: Optional[datetime] = None,
        to_timestamp: Optional[datetime] = None) -> Optional[List[Dict]]:
    col = db[path]
    query = {}
    if action:
        query['action'] = action.value
    if from_timestamp:
        query['timestamp'] = {
            '$gte': from_timestamp
        }
    if to_timestamp:
        query['timestamp'] = {
            **query['timestamp'],
            '$lte': to_timestamp
        }
    return _modify_id(list(col.find(query)))


__all__ = ['get_log', 'log_message']
