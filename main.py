#main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from models import User, Gender, Role
from uuid import UUID, uuid4

app = FastAPI()

db: List[User] = [
    User(
        id=uuid4(),
        first_name="Dev",
        last_name="Ops",
        gender=Gender.other,
        age=21,
        role=Role.student
    ),
    User(
        id=uuid4(),
        first_name="Ops",
        last_name="Dev",
        gender=Gender.other,
        age=44,
        role=Role.working
    )
]

@app.get("/api/v1/users")
async def fetch_users():
    return db;

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return{"id": user.id}
