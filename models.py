from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum 
from uuid import UUID, uuid4

app = FastAPI(openapi_url=None)

class Gender(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class Role(str, Enum):
    student = "Student"
    working = "Working"
    retiree = "Retiree"

class User(BaseModel):
    id: Optional[UUID] = uuid4() 
    first_name: str 
    last_name: str 
    middle_name: Optional[str] = None
    gender: Optional[Gender]
    age: int 
    role: Role