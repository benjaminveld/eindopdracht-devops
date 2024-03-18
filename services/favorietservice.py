from typing import List

from fastapi import HTTPException

from dtos.favorietdtos import FavorietCreateDTO, FavorietDTO
from dtos.livecoinwatchdtos import CoinMapDTO
from models.favoriet import Favoriet
from services.clients import livecoinwatchclient
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
    db_favoriet = db.query(Favoriet).filter(Favoriet.cryptocurrency_id == cryptocurrency.id, Favoriet.user_id == user_id).first()
    if db_favoriet:
        raise HTTPException(status_code=400, detail="Deze cryptocurrency is al een favoriet.")
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


def get_favorieten_overzicht(user_id: int, db) -> List[CoinMapDTO]:
    favorieten = db.query(Favoriet).filter(Favoriet.user_id == user_id).all()
    favorieten_afkortingen = [favoriet.cryptocurrency.afkorting for favoriet in favorieten]
    overzicht_data = livecoinwatchclient.get_coins_informatie(favorieten_afkortingen)
    return overzicht_data
