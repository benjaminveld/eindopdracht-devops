#favoritesdto
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum 

app = FastAPI(openapi_url=None)

class CurrencyDTO(str, Enum): #aanvullen met gegevens uit DB (/ externe api?)
    bitcoin = "btc"
    ethereum = "eth"

class FavoriteDTO(BaseModel):
    id: Optional[str]
    currency: CurrencyDTO