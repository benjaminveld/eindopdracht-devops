from pydantic import BaseModel


class CoinMapDTO(BaseModel):
    naam: str
    afkorting: str
    prijs_in_euro: float
    marktkapitalisatie_in_euro: int
    marktkapitalisatie_rang: int
    leeftijd: int
    all_time_high_in_dollars: float
    aanbod_in_omloop: int
    totaal_aanbod: int
    maximaal_aanbod: int
    volume_in_24_uur: int
    verandering_1_uur: float
    verandering_1_dag: float
    verandering_1_week: float
    verandering_1_maand: float
    verandering_1_jaar: float


class HistoryDTO(BaseModel):
    datum: int
    prijs_in_euro: float