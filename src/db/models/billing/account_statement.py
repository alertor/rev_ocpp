from sqlalchemy import Boolean, Column, Float, DateTime, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


# Monthly/Weekly account statements
class AccountStatement(Base):
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(ForeignKey('account.id'), nullable=False, index=True)
    date = Column(DateTime, nullable=False)
    closing_balance = Column(Float, nullable=False)
    total_credit = Column(Float, nullable=False)
    total_debit = Column(Float, nullable=False)

    account = relationship('Account', back_populates='statements')
