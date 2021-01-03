from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class ChargePoint(Base):
    id = Column(Integer, primary_key=True, index=True)
    model = Column(String(20), nullable=False)
    vendor = Column(String(20), nullable=False)
    serial_number = Column(String(25))
    firmware = Column(String(50))
    type = Column(String(25))
    last_heartbeat = Column(DateTime(True))
    boot_timestamp = Column(DateTime(True))
    identity = Column(String(50), nullable=False, unique=True)
    connected = Column(Boolean, nullable=False)

    connectors = relationship('Connector', back_populates='chargepoint')
