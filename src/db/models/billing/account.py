from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base_class import Base


# Account class exists to allow extensions in the future:
# Multiple users per account / Multiple accounts per user
class Account(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)

    user = relationship('User', back_populates='account')
    debits = relationship('Debit', back_populates='account')
    credits = relationship('Credit', back_populates='account')
    statements = relationship('AccountStatement', back_populates='account')
