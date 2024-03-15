from typing import List

from dtos.favorietdtos import FavorietCreateDTO, FavorietDTO
from models.favoriet import Favoriet
from services.cryptocurrencyservice import map_cryptocurrency, get_or_create_cryptocurrency


def get_favorieten(user_id: int, db) -> List[FavorietDTO]:
    favorieten = db.query(Favoriet).filter(Favoriet.user_id == user_id).all()
    return [map_favoriet(favoriet) for favoriet in favorieten]


def map_favoriet(favoriet: Favoriet) -> FavorietDTO:
    return FavorietDTO(
        id=favoriet.id,
        cryptocurrency=map_cryptocurrency(favoriet.cryptocurrency),
        user_id=favoriet.user_id
    )


def register_favoriet(favoriet: FavorietCreateDTO, user_id: int, db) -> FavorietDTO:
    cryptocurrency = get_or_create_cryptocurrency(favoriet.cryptocurrency, db)
    db_favoriet = Favoriet(
        cryptocurrency_id=cryptocurrency.id,
        user_id=user_id
    )
    db.add(db_favoriet)
    db.commit()
    db.refresh(db_favoriet)
    return map_favoriet(db_favoriet)


def delete_favoriet(favoriet_id: int, user_id: int, db):
    db.query(Favoriet).filter(Favoriet.id == favoriet_id, Favoriet.user_id == user_id).delete()
    db.commit()
