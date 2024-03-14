from pydantic import BaseModel


class UserBase(BaseModel):
    gebruikersnaam: str
    wachtwoord: str


class UserDTO(UserBase):
    id: int


class UserCreateDTO(UserBase):
    pass
