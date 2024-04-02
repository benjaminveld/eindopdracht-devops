import datetime
import itertools

from typing import List
from dtos.transactiedtos import TransactieDTO
from models.transactie import Transactie
from services.clients.livecoinwatchclient import get_coin_if_exists, get_coin_history

from models.cryptocurrency import Cryptocurrency
from dtos.transactiedtos import BalansOverzichtDTO, CryptocurrencyBalansDTO

def get_transacties(user_id: int, db) -> List[TransactieDTO]:
    transacties = db.query(Transactie).filter(Transactie.user_id == user_id).all()
    return [map_transactie(transactie) for transactie in transacties]


def map_transactie(transactie: Transactie) -> TransactieDTO:
    return TransactieDTO(
        id=transactie.id,
        cryptocurrency=transactie.cryptocurrency.naam,
        cryptocurrency_afkorting=transactie.cryptocurrency.afkorting, 
        aantal=transactie.aantal,
        transactie_tijdstip=transactie.transactie_tijdstip,
        user_id=transactie.user_id
    )




def register_transactie(transactie, user_id, db):
    print("Start")
    # Zoek de ID van de cryptocurrency op basis van de naam
    cryptocurrency_id = db.query(Cryptocurrency.id).filter(Cryptocurrency.naam == transactie.cryptocurrency).first()[0]
    
    db_transactie = Transactie(
        cryptocurrency_id=cryptocurrency_id,  # gebruik de id 
        aantal=transactie.aantal,
        user_id=user_id,
        transactie_tijdstip=datetime.datetime.now()
    )
    print("Transactie!!!")
    db.add(db_transactie)
    db.commit()
    db.refresh(db_transactie)

    return map_transactie(db_transactie)




def get_balans_overzicht(user_id: int, db) -> BalansOverzichtDTO:
    transacties = db.query(Transactie).filter(Transactie.user_id == user_id).all()
    transacties = [map_transactie(transactie) for transactie in transacties]
    transacties_by_cryptocurrency_map = itertools.groupby(transacties, key=lambda transactie: transactie.cryptocurrency_afkorting)

    totaal_balans = 0
    totaal_inleg = 0
    cryptocurrencies = []
    for cryptocurrency, transacties in transacties_by_cryptocurrency_map:
        aantal = 0
        inleg = 0
        for transactie in transacties:
            aantal += transactie.aantal
            coin_history_dto = get_coin_history(transactie.cryptocurrency_afkorting, transactie.transactie_tijdstip)
            inleg += transactie.aantal * coin_history_dto.prijs_in_euro
        coin_map_dto = get_coin_if_exists(cryptocurrency)
        balans = aantal * coin_map_dto.prijs_in_euro
        totaal_balans += balans
        totaal_inleg += inleg
        cryptocurrencies.append(CryptocurrencyBalansDTO(
            naam=coin_map_dto.naam,
            aantal=aantal,
            balans_in_euro=balans,
            winst_in_euro=balans - inleg
        ))
    return BalansOverzichtDTO(
        totaal_balans_in_euro=totaal_balans,
        totaal_winst_in_euro=totaal_balans - totaal_inleg,
        cryptocurrencies=cryptocurrencies
    )
