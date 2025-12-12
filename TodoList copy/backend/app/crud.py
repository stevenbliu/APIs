# app/crud.py
from sqlmodel import Session, select
from app.models import User
import logging

logging.basicConfig(
    level=logging.INFO,  # Show INFO and above
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_user(session: Session, email: str, is_superuser: bool = False):
    logger.info("Creating User")
    user = User(email=email, is_superuser=is_superuser)
    session.refresh
    session.add(user)
    session.commit()
    logging.info("does this work")
    session.refresh(user)
    return user


def get_user_by_email(session: Session, email: str):
    return session.exec(select(User).where(User.email == email)).first()
