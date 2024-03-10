from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Transactie(Base):
    __tablename__ = 'TRANSACTIE'
    id = Column(Integer, primary_key=True, index=True)
    cryptocurrency = Column(String, index=True)
    transactie_tijdstip = Column(DateTime(timezone=True), server_default=func.now())
    aantal = Column(Integer)
    user_id = Column(Integer, ForeignKey('USER.id'))
    user = relationship("User", back_populates="transacties")
