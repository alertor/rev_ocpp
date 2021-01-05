from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException
from dateutil import parser


def utc_datetime() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def parse_iso_parameter(iso: Optional[str]) -> Optional[datetime]:
    # If None is passed in, return None
    if iso is None:
        return None
    # If anything else is passed in, attempt to convert to datetime
    try:
        return parser.isoparse(iso)
    except ValueError:
        print(iso)
        raise HTTPException(status_code=400, detail='Invalid timestamp format. Only ISO8601 are supported')
