from db.models import ChargePoint
from db.session import session

from sqlalchemy.orm.exc import NoResultFound


def authenticate_charge_point(identity: str) -> bool:
    with session() as s:
        try:
            s.query(ChargePoint).filter(ChargePoint.identity == identity).one()
        except NoResultFound:
            return False

    return True
