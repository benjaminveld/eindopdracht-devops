from pydantic import BaseModel

from dtos.cryptocurrencydtos import CryptocurrencyDTO


class FavorietBase(BaseModel):
    pass


class FavorietDTO(FavorietBase):
    id: int
    user_id: int
    cryptocurrency: CryptocurrencyDTO


class FavorietCreateDTO(FavorietBase):
    cryptocurrency: str
