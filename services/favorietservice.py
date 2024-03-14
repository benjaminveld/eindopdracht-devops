from typing import List

from dtos.favorietdtos import FavorietCreateDTO, FavorietDTO
from models.favoriet import Favoriet


def get_favorieten(user_id: int, db) -> List[FavorietDTO]:
    favorieten = db.query(Favoriet).filter(Favoriet.user_id == user_id).all()
    return [map_favoriet(favoriet) for favoriet in favorieten]


def map_favoriet(favoriet: Favoriet) -> FavorietDTO:
    return FavorietDTO(
        id=favoriet.id,
        cryptocurrency=favoriet.cryptocurrency,
        user_id=favoriet.user_id
    )


def register_favoriet(favoriet: FavorietCreateDTO, user_id: int, db) -> FavorietDTO:
    db_favoriet = Favoriet(
        cryptocurrency=favoriet.cryptocurrency,
        user_id=user_id
    )
    db.add(db_favoriet)
    db.commit()
    db.refresh(db_favoriet)
    return map_favoriet(db_favoriet)


def delete_favoriet(favoriet_id: int, user_id: int, db):
    db.query(Favoriet).filter(Favoriet.id == favoriet_id, Favoriet.user_id == user_id).delete()
    db.commit()
