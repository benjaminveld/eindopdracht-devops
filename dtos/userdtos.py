from pydantic import BaseModel, constr, validator


class UserBase(BaseModel):
    gebruikersnaam: constr(min_length=2)
    wachtwoord: constr(min_length=2)

    @validator('gebruikersnaam')
    def check_gebruikersnaam_not_null(cls, value):
        if value is None:
            raise ValueError("Gebruikersnaam mag niet leeg zijn")
        return value

    @validator('wachtwoord')
    def check_wachtwoord_not_null(cls, value):
        if value is None:
            raise ValueError("Wachtwoord mag niet leeg zijn")
        return value



class UserDTO(UserBase):
    id: int


class UserCreateDTO(UserBase):
    pass