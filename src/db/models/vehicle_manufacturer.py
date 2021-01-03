from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class VehicleManufacturer(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    models = relationship('VehicleModel', back_populates='manufacturer')
