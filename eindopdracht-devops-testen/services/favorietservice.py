from typing import List

from dtos.favorietdtos import FavorietCreateDTO, FavorietDTO
from models.favoriet import Favoriet
from models.cryptocurrency import Cryptocurrency
from services.clients import livecoinwatchclient
from dtos.livecoinwatchdtos import CoinMapDTO


def get_favorieten(user_id: int, db) -> List[FavorietDTO]:
    favorieten = db.query(Favoriet).filter(Favoriet.user_id == user_id).all()
    return [map_favoriet(favoriet) for favoriet in favorieten]


def map_favoriet(favoriet: Favoriet) -> FavorietDTO:
    return FavorietDTO(
        id=favoriet.id,
        cryptocurrency=favoriet.cryptocurrency.naam,  # Gebruik de naam van de cryptocurrency als string
        user_id=favoriet.user_id
    )


def register_favoriet(favoriet: FavorietCreateDTO, user_id: int, db) -> FavorietDTO:
    # Zoek het Cryptocurrency-object op basis van de naam
    cryptocurrency = db.query(Cryptocurrency).filter(Cryptocurrency.naam == favoriet.cryptocurrency).first()
    if not cryptocurrency:
        # Handel hier de situatie af waarin de cryptocurrency niet wordt gevonden
        raise ValueError(f"Cryptocurrency '{favoriet.cryptocurrency}' not found")

    # Maak het Favoriet-object met het gevonden Cryptocurrency-object
    db_favoriet = Favoriet(
        cryptocurrency=cryptocurrency,
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
