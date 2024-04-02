from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Favoriet(Base):
    __tablename__ = 'FAVORIETEN'
    id = Column(Integer, primary_key=True, index=True,  autoincrement=True)
    cryptocurrency = relationship("Cryptocurrency", back_populates="favorieten")
    cryptocurrency_id = Column(Integer, ForeignKey('CRYPTOCURRENCIES.id'))
    user_id = Column(Integer, ForeignKey('USERS.id'))
    user = relationship("User", back_populates="favorieten")
