from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Favoriet(Base):
    __tablename__ = 'FAVORIET'
    id = Column(Integer, primary_key=True, index=True)
    cryptocurrency = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('USER.id'))
    user = relationship("User", back_populates="favorieten")
