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


def log_connect(point_id: str) -> None:
    col = db['connections']
    col.insert_one({
        'chargepoint_id': point_id,
        'timestamp': utc_datetime()
    })


def log_message(message, path: Optional[str] = None):
    col = db[path if path else 'ocpp_msgs']
    col.insert_one({
        **message,
        'timestamp': utc_datetime()
    })


def get_connection_log(
        from_timestamp: Optional[datetime] = None,
        to_timestamp: Optional[datetime] = None
) -> List[Dict]:
    col = db['connections']
    query = {}
    if from_timestamp:
        query['timestamp'] = {
            '$gte': from_timestamp
        }
    if to_timestamp:
        query['timestamp'] = {
            **query['timestamp'],
            '$lte': to_timestamp
        }
    return list(col.find(query, {'_id': 0}))


def get_message_log(
        path: str,
        actions: Optional[List[Action]] = None,
        from_timestamp: Optional[datetime] = None,
        to_timestamp: Optional[datetime] = None) -> List[Dict]:
    col = db[path]
    query = {}
    if actions:
        query['action'] = {
            '$in': [action.value for action in actions]
        }
    if from_timestamp:
        query['timestamp'] = {
            '$gte': from_timestamp
        }
    if to_timestamp:
        query['timestamp'] = {
            **query['timestamp'],
            '$lte': to_timestamp
        }
    return list(col.find(query, {'_id': 0}))


__all__ = ['get_connection_log', 'get_message_log', 'log_connect', 'log_message']
