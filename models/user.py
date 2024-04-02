from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from .favoriet import Favoriet
from .transactie import Transactie


class User(Base):
    __tablename__ = 'USERS'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gebruikersnaam = Column(String, index=True)
    wachtwoord = Column(String)
    favorieten = relationship("Favoriet", back_populates="user")
    transacties = relationship("Transactie", back_populates="user")
