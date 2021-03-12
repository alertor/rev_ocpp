from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from db.base_class import Base


class Debit(Base):
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(ForeignKey('account.id'), nullable=False, index=True)
    transaction_id = Column(ForeignKey('transaction.id'), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime(True), nullable=False)

    account = relationship('Account', back_populates='debits')
