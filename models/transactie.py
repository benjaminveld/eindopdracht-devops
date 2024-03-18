from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from .base import Base


class Transactie(Base):
    __tablename__ = 'TRANSACTIE'
    id = Column(Integer, primary_key=True, index=True)
    cryptocurrency = relationship("Cryptocurrency", back_populates="transacties")
    cryptocurrency_id = Column(Integer, ForeignKey('CRYPTOCURRENCY.id'))
    transactie_tijdstip = Column(DateTime(timezone=True), server_default=func.now())
    aantal = Column(Numeric(60, 30))
    user_id = Column(Integer, ForeignKey('USER.id'))
    user = relationship("User", back_populates="transacties")
