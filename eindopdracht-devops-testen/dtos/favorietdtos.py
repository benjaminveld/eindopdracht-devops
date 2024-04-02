from pydantic import BaseModel


class FavorietBase(BaseModel):
    cryptocurrency: str


class FavorietDTO(FavorietBase):
    id: int
    user_id: int
    cryptocurrency: str  # Voeg dit veld toe om validatiefouten te voorkomen


class FavorietCreateDTO(FavorietBase):
    pass
