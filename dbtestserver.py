#!/usr/bin/env python3
from fastapi import FastAPI, Depends
from models.user import User
from database import SessionLocal


# FastAPI app initialization
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Test endpoint to retrieve all users from db
@app.get("/users/")
def read_users(db=Depends(get_db)):
    users = db.query(User).all()
    return users
