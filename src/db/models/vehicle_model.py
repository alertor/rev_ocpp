from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class VehicleModel(Base):
    id = Column(Integer, primary_key=True, index=True)
    manufacturer_id = Column(ForeignKey('vehiclemanufacturer.id'), index=True, nullable=True)
    model = Column(String(50))

    manufacturer = relationship('VehicleManufacturer', back_populates='models')
