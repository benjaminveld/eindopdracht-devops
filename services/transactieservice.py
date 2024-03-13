import datetime
from typing import List

from dtos.transactiedtos import TransactieDTO
from models.transactie import Transactie


def get_transacties(user_id: int, db) -> List[TransactieDTO]:
    transacties = db.query(Transactie).filter(Transactie.user_id == user_id).all()
    return [map_transactie(transactie) for transactie in transacties]


def map_transactie(transactie: Transactie) -> TransactieDTO:
    return TransactieDTO(
        id=transactie.id,
        cryptocurrency=transactie.cryptocurrency,
        aantal=transactie.aantal,
        transactie_tijdstip=transactie.transactie_tijdstip,
        user_id=transactie.user_id
    )


def register_transactie(transactie, user_id, db):
    db_transactie = Transactie(
        cryptocurrency=transactie.cryptocurrency,
        aantal=transactie.aantal,
        user_id=user_id,
        transactie_tijdstip = datetime.datetime.now()
    )
    db.add(db_transactie)
    db.commit()
    db.refresh(db_transactie)
    return map_transactie(db_transactie)
