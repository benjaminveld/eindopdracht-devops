#transactionsdto
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4
from favoritesdto.py import CurrencyDTO

app = FastAPI(openapi_url=None)

class TransactionDTO(BaseModel):
    id: Optional[UUID] = uuid4()
    currency: CurrencyDTO
    amount: int

