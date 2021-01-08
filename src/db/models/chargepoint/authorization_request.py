from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class AuthorizationRequest(Base):
    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(ForeignKey('token.id'), index=True, nullable=True)
    chargepoint_id = Column(ForeignKey('chargepoint.id'), nullable=False, index=True)
    token_string = Column(String(20))
    timestamp = Column(DateTime(True), nullable=False)

    token = relationship('Token')
    chargepoint = relationship('ChargePoint')
