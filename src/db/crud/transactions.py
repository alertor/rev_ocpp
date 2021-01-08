from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from .. import models, schemas


def get_transactions_by_datetime(
        db: Session,
        start_timestamp: Optional[datetime] = None,
        end_timestamp: Optional[datetime] = None,
        meter_over: Optional[int] = None) -> List[schemas.Transaction]:

    query = db.query(models.Transaction)

    # Apply time filters
    if start_timestamp:
        query = query.filter(
            models.Transaction.start_timestamp > start_timestamp
        )
    if end_timestamp:
        query = query.filter(
            models.Transaction.end_timestamp < end_timestamp
        )
    # Apply meter filters
    if meter_over:
        query = query.filter(
            models.Transaction.meter_used > meter_over
        )

    return query.all()
