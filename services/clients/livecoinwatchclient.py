import json
import os
from datetime import datetime

import requests
from typing import List

from dotenv import load_dotenv
from fastapi import HTTPException

from dtos.livecoinwatchdtos import CoinMapDTO, HistoryDTO

load_dotenv()

API_KEY = os.getenv('LIVECOINWATCH_API_KEY')
URL = "https://api.livecoinwatch.com"
headers = {
  'content-type': 'application/json',
  'x-api-key': API_KEY
}


def get_coin_if_exists(afkorting: str) -> CoinMapDTO:
    coins = get_coins_informatie([afkorting])
    if not coins:
        raise HTTPException(status_code=400, detail="Deze cryptocurrency bestaat niet. Maak gebruikt van de afkorting van de cryptocurrency (E.g. BTC, ETH, VET).")
    return coins[0]


def map_coin(cryptocurrency) -> CoinMapDTO:
    return CoinMapDTO(
        naam=cryptocurrency['name'],
        afkorting=cryptocurrency['code'],
        prijs_in_euro=float(cryptocurrency['rate']),
        marktkapitalisatie_in_euro=int(cryptocurrency['cap']),
        marktkapitalisatie_rang=int(cryptocurrency['rank']),
        leeftijd=int(cryptocurrency['age']),
        all_time_high_in_dollars=float(cryptocurrency['allTimeHighUSD']),
        aanbod_in_omloop=int(cryptocurrency['circulatingSupply']),
        totaal_aanbod=int(cryptocurrency['totalSupply']),
        maximaal_aanbod=-1 if cryptocurrency['maxSupply'] is None else int(cryptocurrency['maxSupply']),
        volume_in_24_uur=int(cryptocurrency['volume']),
        verandering_1_uur=float(cryptocurrency['delta']['hour']),
        verandering_1_dag=float(cryptocurrency['delta']['day']),
        verandering_1_week=float(cryptocurrency['delta']['week']),
        verandering_1_maand=float(cryptocurrency['delta']['month']),
        verandering_1_jaar=float(cryptocurrency['delta']['year'])
    )


def map_history(history) -> HistoryDTO:
    return HistoryDTO(
        datum=int(history['date']),
        prijs_in_euro=float(history['rate'])
    )


def get_coins_informatie(coin_afkortingen: List[str]) -> List[CoinMapDTO]:
    if not coin_afkortingen:
        return []

    payload = json.dumps({
      "codes": coin_afkortingen,
      "currency": "EUR",
      "sort": "rank",
      "order": "ascending",
      "offset": 0,
      "limit": 0,
      "meta": True
    })

    response = requests.request("POST", URL+"/coins/map", headers=headers, data=payload)

    if response.status_code == 200:
        cryptocurrencies = response.json()
        return [map_coin(cryptocurrency) for cryptocurrency in cryptocurrencies]
    else:
        #TODO: logging
        print(response)
        raise HTTPException(status_code=503, detail="Livecoinwatch API is niet beschikbaar. Probeer het later opnieuw.")


def get_coin_history(afkorting: str, tijdstip: datetime) -> HistoryDTO:
    payload = json.dumps({
        "code": afkorting,
        "currency": "EUR",
        "start": tijdstip.timestamp() * 1000,
        "end": tijdstip.timestamp() * 1000 + 100000000,
        "meta": False
    })

    response = requests.request("POST", URL+"/coins/single/history", headers=headers, data=payload)

    if response.status_code == 200:
        histories = response.json()
        return map_history(histories['history'][0])
    else:
        # TODO: logging
        print(response.__dict__)
        raise HTTPException(status_code=503, detail="Livecoinwatch API is niet beschikbaar. Probeer het later opnieuw.")


