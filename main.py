#main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from models import UserDTO, GenderDTO, RoleDTO, FavoriteDTO, TransactionDTO
from uuid import UUID, uuid4

app = FastAPI()

userdb: List[UserDTO] = [
    UserDTO(
        id=uuid4(),
        first_name="Dev",
        last_name="Ops",
        gender=GenderDTO.other,
        age=21,
        role=RoleDTO.student
    ),
    UserDTO(
        id=uuid4(),
        first_name="Ops",
        last_name="Dev",
        gender=GenderDTO.other,
        age=44,
        role=RoleDTO.working
    )
]

favoritedb: List[FavoriteDTO]= [

]

transactiondb: List[TransactionDTO]= [

]

@app.get("/api/v1/users")
async def fetch_users():
    return userdb;

@app.post("/api/v1/users")
async def register_user(user: UserDTO):
    userdb.append(user)
    return{"id": user.id}\

@app.get("/api/v1/favorites")
async def fetch_favorite():
    return favoritedb

@app.post("/api/v1/favorites")
async def register_favorites(favorite: FavoriteDTO):
    favoritedb.append(favorite)
    return{"favorite": favorite.currency}

@app.get("/api/v1/transactions")
async def fetch_transactions():
    return transactiondb

@app.post("/api/v1/transactions")
async def register_transaction(transaction: TransactionDTO):
    transactiondb.append(transaction)
    return{"transaction amount": transaction.amount, "currency": transaction.currency }