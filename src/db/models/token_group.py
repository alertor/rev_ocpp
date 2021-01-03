from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class TokenGroup(Base):
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(20), nullable=False, unique=True)

    tokens = relationship('Token', back_populates='token_group')
