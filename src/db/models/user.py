from sqlalchemy import Boolean, Column, DateTime, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base

vehicle_users = Table(
    'vehicle_users', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('vehicle_id', Integer, ForeignKey('vehicle.id'))
  )


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime(True))
    is_superuser = Column(Boolean, nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False, unique=True)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    date_joined = Column(DateTime(True), nullable=False)

    tokens = relationship('Token', back_populates='user')
    vehicles = relationship(
        'Vehicle',
        secondary=vehicle_users,
        back_populates='users'
    )