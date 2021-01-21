from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base_class import Base


class InProgressTransaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    start_timestamp = Column(DateTime(True), nullable=False)
    meter_start = Column(Integer, nullable=False)
    reservation_id = Column(Integer)
    connector_id = Column(ForeignKey('connector.id'), nullable=False, index=True)
    start_token_id = Column(ForeignKey('token.id'), nullable=True, index=True)

    connector = relationship('Connector')
    start_token = relationship('Token')
