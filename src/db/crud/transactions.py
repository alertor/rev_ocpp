from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from .. import models, schemas


def get_transactions_by_datetime(
        db: Session,
        start_timestamp: Optional[datetime] = None,
        end_timestamp: Optional[datetime] = None) -> List[schemas.Transaction]:
    if start_timestamp and end_timestamp:
        return db.query(models.Transaction).filter(
            models.Transaction.start_timestamp.between(start_timestamp, end_timestamp)
        ).all()
    elif start_timestamp:
        return db.query(models.Transaction).filter(
            models.Transaction.start_timestamp > start_timestamp
        ).all()
    elif end_timestamp:
        return db.query(models.Transaction).filter(
            models.Transaction.start_timestamp < end_timestamp
        ).all()
    else:
        return db.query(models.Transaction).all()
