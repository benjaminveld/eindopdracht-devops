from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TransactieBase(BaseModel):
    cryptocurrency: str
    aantal: int


class TransactieDTO(BaseModel):
    id: int
    cryptocurrency: str
    cryptocurrency_afkorting: Optional[str]  # Nieuw toegevoegd attribuut
    aantal: float
    transactie_tijdstip: datetime
    user_id: int


class TransactieCreateDTO(TransactieBase):
    pass


class CryptocurrencyBalansDTO(BaseModel):
    naam: str
    aantal: float
    balans_in_euro: float
    winst_in_euro: float


class BalansOverzichtDTO(BaseModel):
    totaal_balans_in_euro: float
    totaal_winst_in_euro: float
    cryptocurrencies: list[CryptocurrencyBalansDTO]