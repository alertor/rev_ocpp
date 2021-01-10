from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from .. import models, schemas


def get_transactions(
        db: Session,
        from_timestamp: Optional[datetime] = None,
        to_timestamp: Optional[datetime] = None,
        meter_over: Optional[int] = None) -> List[schemas.Transaction]:

    query = db.query(models.Transaction)

    # Apply time filters
    if from_timestamp:
        query = query.filter(
            models.Transaction.start_timestamp > from_timestamp
        )
    if to_timestamp:
        query = query.filter(
            models.Transaction.end_timestamp < to_timestamp
        )

    # Apply meter filters
    if meter_over:
        query = query.filter(
            models.Transaction.meter_used > meter_over
        )

    return query.all()
