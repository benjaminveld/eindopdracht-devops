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
