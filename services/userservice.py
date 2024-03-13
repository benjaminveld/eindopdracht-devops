from typing import List

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
