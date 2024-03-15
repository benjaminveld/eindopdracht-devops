from pydantic import BaseModel


class CryptocurrencyBase(BaseModel):
    naam: str
    afkorting: str


class CryptocurrencyDTO(CryptocurrencyBase):
    id: int
