import datetime
from typing import List

from fastapi import HTTPException

from dtos.cryptocurrencydtos import CryptocurrencyDTO
from dtos.transactiedtos import TransactieDTO, TransactieCreateDTO
from models.cryptocurrency import Cryptocurrency
from models.transactie import Transactie
from services.cryptocurrencyservice import map_cryptocurrency, get_or_create_cryptocurrency


def get_transacties(user_id: int, db) -> List[TransactieDTO]:
    transacties = db.query(Transactie).filter(Transactie.user_id == user_id).all()
    return [map_transactie(transactie) for transactie in transacties]


def map_transactie(transactie: Transactie) -> TransactieDTO:
    return TransactieDTO(
        id=transactie.id,
        cryptocurrency=map_cryptocurrency(transactie.cryptocurrency),
        aantal=transactie.aantal,
        transactie_tijdstip=transactie.transactie_tijdstip,
        user_id=transactie.user_id
    )


def register_transactie(transactie: TransactieCreateDTO, user_id: int, db):
    cryptocurrency = valideer_transactie(transactie, user_id, db)
    db_transactie = Transactie(
        cryptocurrency_id=cryptocurrency.id,
        aantal=transactie.aantal,
        user_id=user_id,
        transactie_tijdstip=datetime.datetime.now()
    )
    db.add(db_transactie)
    db.commit()
    db.refresh(db_transactie)
    return map_transactie(db_transactie)


def valideer_transactie(transactie: TransactieCreateDTO, user_id: int, db) -> CryptocurrencyDTO:
    cryptocurrency = get_or_create_cryptocurrency(transactie.cryptocurrency, db)
    if get_totaal_aantal(transactie.cryptocurrency, user_id, db) + transactie.aantal < 0:
        raise HTTPException(status_code=400, detail="Je verkoopt te veel. Je eindbalans kan niet negatief zijn.")
    return cryptocurrency


def get_totaal_aantal(cryptocurrency: str, user_id: int, db) -> float:
    transacties = (db.query(Transactie)
                   .join(Transactie.cryptocurrency)
                   .filter(Transactie.user_id == user_id, Cryptocurrency.afkorting == cryptocurrency)
                   .all())
    totaal = 0
    for transactie in transacties:
        totaal += float(transactie.aantal)
    return totaal
