from typing import List

from fastapi import HTTPException

from dtos.userdtos import UserDTO, UserCreateDTO
from models.user import User


def get_users(db) -> List[UserDTO]:
    users = db.query(User).all()
    return [map_user(user) for user in users]


def map_user(user: User) -> UserDTO:
    return UserDTO(
        id=user.id,
        gebruikersnaam=user.gebruikersnaam,
        wachtwoord=user.wachtwoord
    )


def register_user(user: UserCreateDTO, db) -> UserDTO:
    db_user = User(
        gebruikersnaam=user.gebruikersnaam,
        wachtwoord=user.wachtwoord
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return map_user(db_user)


def get_logged_in_user(token: str, db) -> UserDTO:
    db_user = db.query(User).filter(User.gebruikersnaam == token).first()
    return map_user(db_user)


def authenticate_user(gebruikersnaam: str, wachtwoord: str, db) -> UserDTO:
    user_db = db.query(User).filter(User.gebruikersnaam == gebruikersnaam).first()
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not wachtwoord == user_db.wachtwoord:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return map_user(user_db)