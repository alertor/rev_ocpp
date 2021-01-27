from datetime import datetime, timedelta
from typing import Dict, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.util import KeyedTuple

import db.models as models
import db.schemas as schemas

from util import utc_datetime

from .types import BucketType


def get_usage(
        db: Session,
        kwh: bool = True,
        count: bool = True,
        bucket: BucketType = BucketType.Days,
        chargepoint: str = None,
        from_timestamp: Optional[datetime] = None,
        to_timestamp: Optional[datetime] = None) -> List[KeyedTuple]:
    """
    Get the usage of the charging stations
    """

    args = [func.date(models.Transaction.start_timestamp).label('date')]
    if count:
        args.append(func.count(models.Transaction.id).label('count'))
    if kwh:
        args.append(func.sum(models.Transaction.meter_used).label('kwh'))

    query = db.query(*args)

    if chargepoint:
        # Transaction -> Connector -> ChargePoint
        query = query.filter(models.Transaction.connector.has(
            models.Connector.chargepoint.has(
                models.ChargePoint.identity == chargepoint
            )
        ))

    # Apply time filters
    if from_timestamp:
        query = query.filter(
            models.Transaction.start_timestamp > from_timestamp
        )
    if to_timestamp:
        query = query.filter(
            models.Transaction.end_timestamp < to_timestamp
        )

    # Generate date series
    timeseries = db.query(
        func.date(func.generate_series(
            func.min(from_timestamp or models.Transaction.start_timestamp),
            func.max(to_timestamp or utc_datetime()),
            timedelta(days=1))
        ).label('date')
    ).subquery()

    # Group values
    data = query.group_by('date').subquery()
    values = []
    if count:
        values.append(func.coalesce(data.c.count, 0).label('count'))
    if kwh:
        values.append(func.coalesce(data.c.kwh, 0).label('kWh'))

    return db.query(timeseries.c.date, *values).\
        outerjoin(data, data.c.date == timeseries.c.date).\
        order_by(timeseries.c.date).all()


