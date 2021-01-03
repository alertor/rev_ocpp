from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.orm import relationship

from db.base_class import Base


class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer)
    start_timestamp = Column(DateTime(True), nullable=False)
    end_timestamp = Column(DateTime(True), nullable=False)
    duration = Column(INTERVAL, nullable=False)
    meter_start = Column(Integer, nullable=False)
    meter_stop = Column(Integer, nullable=False)
    meter_used = Column(Integer, nullable=False)
    stop_reason = Column(Text)
    connector_id = Column(ForeignKey('connector.id'), nullable=True, index=True)
    end_token_id = Column(ForeignKey('token.id'), nullable=True, index=True)
    start_token_id = Column(ForeignKey('token.id'), nullable=True, index=True)

    connector = relationship('Connector')
    end_token = relationship('Token', primaryjoin='Transaction.end_token_id == Token.id')
    start_token = relationship('Token', primaryjoin='Transaction.start_token_id == Token.id')
