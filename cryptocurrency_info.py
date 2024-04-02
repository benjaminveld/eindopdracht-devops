from sqlalchemy import Column, Integer, String, Float
from test.models.base import Base

class CryptocurrencyInfo(Base):
    __tablename__ = 'cryptocurrency_info'
    id = Column(Integer, primary_key=True, index=True)
    naam = Column(String)
    afkorting = Column(String)
    prijs_in_euro = Column(Float)
    marktkapitalisatie_in_euro = Column(Float)
    marktkapitalisatie_rang = Column(Integer)
    leeftijd = Column(Integer)
    all_time_high_in_dollars = Column(Float)
    aanbod_in_omloop = Column(Integer)
    totaal_aanbod = Column(Integer)
    maximaal_aanbod = Column(Integer)
    volume_in_24_uur = Column(Float)
    verandering_1_uur = Column(Float)
    verandering_1_dag = Column(Float)
    verandering_1_week = Column(Float)
    verandering_1_maand = Column(Float)
    verandering_1_jaar = Column(Float)
