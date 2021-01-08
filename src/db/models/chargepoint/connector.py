from sqlalchemy import Boolean, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from db.base_class import Base


class Connector(Base):
    __table_args__ = (
        UniqueConstraint('connector_id', 'chargepoint_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    connector_id = Column(Integer, nullable=False)
    chargepoint_id = Column(ForeignKey('chargepoint.id'), nullable=False, index=True)
    available = Column(Boolean, nullable=False)
    in_use = Column(Boolean, nullable=False)

    chargepoint = relationship('ChargePoint', back_populates='connectors')
