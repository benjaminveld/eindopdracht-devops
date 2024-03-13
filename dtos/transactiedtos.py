from datetime import datetime

from pydantic import BaseModel


class TransactieBase(BaseModel):
    cryptocurrency: str
    aantal: int


class TransactieDTO(TransactieBase):
    id: int
    transactie_tijdstip: datetime
    user_id: int


class TransactieCreateDTO(TransactieBase):
    pass
