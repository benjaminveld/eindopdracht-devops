from pydantic import BaseModel


class FavorietBase(BaseModel):
    cryptocurrency: str


class FavorietDTO(FavorietBase):
    id: int
    user_id: int


class FavorietCreateDTO(FavorietBase):
    pass
