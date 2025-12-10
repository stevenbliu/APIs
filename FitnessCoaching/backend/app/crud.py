# app/crud.py
from sqlmodel import Session, select
from app.models import (
    User,
    UserCreate,
    Session as ModelSession,
    ProgramExercise,
    Program,
)
import logging

logging.basicConfig(
    level=logging.INFO,  # Show INFO and above
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_user(session: Session, user_create: UserCreate):
    user = User(name=user_create.name)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user_name(session: Session, user_id: int, new_name: str):
    user = session.get(User, user_id)
    if user:
        user.name = new_name
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def get_user_by_id(session: Session, user_id: int):
    return session.exec(select(User).where(User.id == user_id)).first()


def list_user_sessions(session: Session, user_id: int):
    return session.exec(
        select(ModelSession).where(ModelSession.user_id == user_id)
    ).all()


def add_exercise_to_program(session: Session, program_id: int, exercise_id: int):
    with session.begin():
        pe = ProgramExercise(program_id=program_id, exercise_id=exercise_id)
        session.add(pe)

        program = session.get(Program, program_id)
        if program:
            program.total_exercises += 1
            session.add(program)

    return pe


# # TODO:
# Error handling

# Check for existence before updating/deleting

# Handle unique constraints (e.g., email)

# Raise appropriate exceptions for endpoints to catch

# 8️⃣ Optional / advanced

# Pagination support (limit, offset)

# Sorting/filtering

# Search queries (e.g., search exercises by name)

# Soft/hard delete distinction

# Logging every CRUD operation for debugging/audit
