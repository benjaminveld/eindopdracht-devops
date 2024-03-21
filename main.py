from typing import List, Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from database import SessionLocal
from dtos.favorietdtos import FavorietCreateDTO, FavorietDTO
from dtos.livecoinwatchdtos import CoinMapDTO
from dtos.transactiedtos import TransactieDTO, TransactieCreateDTO, BalansOverzichtDTO
from dtos.userdtos import UserDTO, UserCreateDTO
from services import userservice, favorietservice, transactieservice

from logger import logger
from middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db=Depends(get_db)) -> UserDTO:
    user = userservice.get_logged_in_user(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.get("/api/v1/users")
async def get_users(db=Depends(get_db)) -> List[UserDTO]:
    return userservice.get_users(db)


@app.post("/api/v1/users", status_code=201)
async def register_user(user: UserCreateDTO, db=Depends(get_db)) -> UserDTO:
    return userservice.register_user(user, db)


@app.get("/api/v1/favorieten")
async def get_favorieten(current_user: Annotated[UserDTO, Depends(get_current_user)], db=Depends(get_db)) -> List[FavorietDTO]:
    return favorietservice.get_favorieten(current_user.id, db)


@app.post("/api/v1/favorieten", status_code=201)
async def register_favoriet(current_user: Annotated[UserDTO, Depends(get_current_user)], favoriet: FavorietCreateDTO, db=Depends(get_db)) -> FavorietDTO:
    return favorietservice.register_favoriet(favoriet, current_user.id, db)


@app.delete("/api/v1/favorieten/{favoriet_id}", status_code=204)
async def delete_favoriet(favoriet_id: int, current_user: Annotated[UserDTO, Depends(get_current_user)], db=Depends(get_db)):
    favorietservice.delete_favoriet(favoriet_id, current_user.id, db)


@app.get("/api/v1/transacties")
async def get_transacties(current_user: Annotated[UserDTO, Depends(get_current_user)], db=Depends(get_db)) -> List[TransactieDTO]:
    return transactieservice.get_transacties(current_user.id, db)


@app.post("/api/v1/transacties", status_code=201)
async def register_transactie(transactie: TransactieCreateDTO, current_user: Annotated[UserDTO, Depends(get_current_user)], db=Depends(get_db)) -> TransactieDTO:
    return transactieservice.register_transactie(transactie, current_user.id, db)


@app.get("/api/v1/favorieten/overzicht")
async def get_favorieten_overzicht(current_user: Annotated[UserDTO, Depends(get_current_user)], db=Depends(get_db)) -> List[CoinMapDTO]:
    return favorietservice.get_favorieten_overzicht(current_user.id, db)


@app.get("/api/v1/transacties/balans")
async def get_transactie_overzicht(current_user: Annotated[UserDTO, Depends(get_current_user)], db=Depends(get_db)) -> BalansOverzichtDTO:
    return transactieservice.get_balans_overzicht(current_user.id, db)


@app.post("/token", include_in_schema=False)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)):
    user = userservice.authenticate_user(form_data.username, form_data.password, db)
    return {"access_token": user.gebruikersnaam, "token_type": "bearer"}
