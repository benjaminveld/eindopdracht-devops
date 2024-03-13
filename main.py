from typing import List

from fastapi import FastAPI, Depends

from database import SessionLocal
from dtos.favorietdtos import FavorietCreateDTO, FavorietDTO
from dtos.transactiedtos import TransactieDTO, TransactieCreateDTO
from dtos.userdtos import UserDTO, UserCreateDTO
from services import userservice, favorietservice, transactieservice

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/users")
async def get_users(db=Depends(get_db)) -> List[UserDTO]:
    return userservice.get_users(db)


@app.post("/api/v1/users")
async def register_user(user: UserCreateDTO, db=Depends(get_db)) -> UserDTO:
    return userservice.register_user(user, db)


@app.get("/api/v1/favorieten")
async def get_favorieten(db=Depends(get_db)) -> List[FavorietDTO]:
    return favorietservice.get_favorieten(1, db)


@app.post("/api/v1/favorieten")
async def register_favoriet(favoriet: FavorietCreateDTO, db=Depends(get_db)) -> FavorietDTO:
    return favorietservice.register_favoriet(favoriet, 1, db)


@app.delete("/api/v1/favorieten/{favoriet_id}", status_code=204)
async def delete_favoriet(favoriet_id: int, db=Depends(get_db)):
    favorietservice.delete_favoriet(favoriet_id, 1, db)


@app.get("/api/v1/transacties")
async def get_transacties(db=Depends(get_db)) -> List[TransactieDTO]:
    return transactieservice.get_transacties(1, db)


@app.post("/api/v1/transacties")
async def register_transactie(transactie: TransactieCreateDTO, db=Depends(get_db)) -> TransactieDTO:
    return transactieservice.register_transactie(transactie, 1, db)
