from datetime import datetime

from pydantic import BaseModel

from dtos.cryptocurrencydtos import CryptocurrencyDTO


class TransactieBase(BaseModel):
    aantal: float


class TransactieDTO(TransactieBase):
    id: int
    transactie_tijdstip: datetime
    user_id: int
    cryptocurrency: CryptocurrencyDTO


class TransactieCreateDTO(TransactieBase):
    cryptocurrency: str


class CryptocurrencyBalansDTO(BaseModel):
    naam: str
    aantal: float
    balans_in_euro: float
    winst_in_euro: float


class BalansOverzichtDTO(BaseModel):
    totaal_balans_in_euro: float
    totaal_winst_in_euro: float
    cryptocurrencies: list[CryptocurrencyBalansDTO]
