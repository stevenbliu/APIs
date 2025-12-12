# app/db.py
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./app.db"  # or your Postgres/MySQL URL

# Default engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=True,  # logs SQL queries
    pool_size=5,  # max connections in pool
    max_overflow=10,  # additional connections beyond pool_size
)


def get_session():
    """Yields a SQLModel session for dependency injection in FastAPI."""
    with Session(engine) as session:
        yield session


# Alembic replaces this
def init_db():
    """Create tables initially"""
    print("Reset Tables")
    SQLModel.metadata.drop_all(engine)  # create tables
    SQLModel.metadata.create_all(engine)  # create tables
    # maybe create a superuser


init_db()
