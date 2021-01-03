from db.session import session
from db.models import TestObject
from util import utc_datetime

from ocpp.v16.enums import ChargePointErrorCode


def add():
    with session() as s:
        t = TestObject(
            id=4,
            value=123,
            data='123213',
            time=utc_datetime()
        )

        s.add(t)
        s.commit()


def get():
    with session() as s:
        item = s.query(TestObject).filter(TestObject.id==3).one()
        print(item.data)


def ok():
    a = ChargePointErrorCode.connector_lock_failure

    print(str(a.value))


ok()
