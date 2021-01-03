from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Token(Base):
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(20), nullable=False, unique=True)
    token_group_id = Column(ForeignKey('tokengroup.id'), index=True)
    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)

    token_group = relationship('TokenGroup', back_populates='tokens')
    user = relationship('User', back_populates='tokens')
