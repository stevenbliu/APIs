# conftest.py
import pytest
from sqlmodel import SQLModel, create_engine, Session
from app.models import User, Item
import logging

# Configure logging once for all tests
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@pytest.fixture
def session():
    # In-memory SQLite DB (clean every test)
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
