# app/routes/users.py
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db import get_session

# from app.models import User
from app.crud import create_user, get_user_by_email

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def add_user(email: str, session: Session = Depends(get_session)):
    existing = get_user_by_email(session, email)
    if existing:
        return {"error": "User already exists"}
    user = create_user(session, email)
    return user


@router.get("/")
def get_all_users(session: Session = Depends(get_session)):
    users = {"name": "asdasdas"}
    return users


@router.get("/{email}")
def get_user(email: str, session: Session = Depends(get_session)):
    existing = get_user_by_email(session, email)
    if existing:
        return {"error": "User already exists"}
    user = create_user(session, email)
    return user
