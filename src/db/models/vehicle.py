from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base
from .user import vehicle_users


class Vehicle(Base):
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(ForeignKey('vehiclemodel.id'), index=True)
    registration = Column(String(20), nullable=False)
    owner = Column(ForeignKey('user.id'), nullable=False)

    users = relationship(
        'User',
        secondary=vehicle_users,
        back_populates='vehicles'
    )
