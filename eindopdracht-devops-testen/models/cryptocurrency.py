from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Cryptocurrency(Base):
    __tablename__ = 'CRYPTOCURRENCIES'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    naam = Column(String)
    afkorting = Column(String, index=True)
    favorieten = relationship("Favoriet", back_populates="cryptocurrency")
    transacties = relationship("Transactie", back_populates="cryptocurrency")
    

    
