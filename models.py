from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum 
from uuid import UUID, uuid4

app = FastAPI(openapi_url=None)

class GenderDTO(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class RoleDTO(str, Enum):
    student = "Student"
    working = "Working"
    retiree = "Retiree"

class CurrencyDTO(str, Enum): #even om te testen
    bitcoin = "btc"
    ethereum = "eth"

class UserDTO(BaseModel):
    id: Optional[UUID] = uuid4() 
    first_name: str 
    last_name: str 
    middle_name: Optional[str] = None
    gender: Optional[GenderDTO]
    age: int 
    role: RoleDTO

class FavoriteDTO(BaseModel):
    id: Optional[str]
    currency: CurrencyDTO