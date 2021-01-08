from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class ChargePointError(Base):
    id = Column(Integer, primary_key=True, index=True)
    connector_id = Column(ForeignKey('connector.id'), index=True)
    error_code = Column(String(50))
    info = Column(String(50))
    status = Column(String(50))
    timestamp = Column(DateTime(True), nullable=False)
    vendor_id = Column(String(255))
    vendor_error_code = Column(String(50))

    connector = relationship('Connector')
