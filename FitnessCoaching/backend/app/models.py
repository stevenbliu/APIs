from sqlmodel import Field, SQLModel, TIMESTAMP, Column
from datetime import datetime

# from pydantic import EmailStr


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        sa_column=Column(TIMESTAMP, nullable=False, onupdate=datetime.utcnow),
        default_factory=datetime.utcnow,
    )


class UserCreate(SQLModel):
    name: str


class Coach(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, nullable=False)
    # programs: list["Program"] = Relationship(back_populates="coach")


class Program(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    coach_id: int = Field(foreign_key="coach.id")
    # coach: "Coach" = Relationship(back_populates='programs') # ORM relationships
    total_exercises: int = Field(default=0)


class Exercise(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, nullable=False)
    reps: int = Field(default=12)
    sets: int = Field(default=4)
    image: str | None = Field(default=None)  # S3 URL


class ProgramExercise(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    program_id: int = Field(foreign_key="program.id", ondelete="CASCADE")
    exercise_id: int = Field(foreign_key="exercise.id", ondelete="CASCADE")


class Session(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    program_id: int = Field(foreign_key="program.id")
    progress: float = Field(default=0)


class SessionExercise(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="session.id")
    exercise_id: int = Field(foreign_key="exercise.id")
    completed: bool = Field(default=False)
