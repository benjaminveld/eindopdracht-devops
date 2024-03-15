from dtos.cryptocurrencydtos import CryptocurrencyDTO
from models.cryptocurrency import Cryptocurrency


def map_cryptocurrency(cryptocurrency: Cryptocurrency) -> CryptocurrencyDTO:
    return CryptocurrencyDTO(
        id=cryptocurrency.id,
        naam=cryptocurrency.naam,
        afkorting=cryptocurrency.afkorting
    )


def get_or_create_cryptocurrency(cryptocurrency: str, db) -> CryptocurrencyDTO:
    db_cryptocurrency = db.query(Cryptocurrency).filter(Cryptocurrency.afkorting == cryptocurrency).first()
    if db_cryptocurrency is None:
        db_cryptocurrency = Cryptocurrency(
            naam="temptotdatexterneapibestaat",
            afkorting=cryptocurrency
        )
        db.add(db_cryptocurrency)
        db.commit()
        db.refresh(db_cryptocurrency)
    return map_cryptocurrency(db_cryptocurrency)
