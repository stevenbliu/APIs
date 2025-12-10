# APIs

This repo is meant to get practice with implementing APIs + DBs. Experiemnt with different frameworks, languages, and tools.

## Commands to use when setting up a project

### Env Setup

conda create -n APIs python=3.13
conda activate APIs

### Install depdenncies

pip install fastapi uvicorn sqlmodel alembic python-dotenv pytest

### Init Alembic (in backend dir)

alembic init alembic

### Configure alembic.ini

sqlalchemy.url = sqlite:///./app.db
or postgres_url

### Configure alembic/env.py

from sqlmodel import SQLModel
from app.models import \* # import all your models

target_metadata = SQLModel.metadata

### Define app/models.py

from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
id: int | None = Field(default=None, primary_key=True)
email: str
is_superuser: bool = False

### After updating model.py

alembic revision --autogenerate -m "sample message"
alembic upgrade head

### Define app/main.py

from fastapi import FastAPI
from app.models import User
from app.db import engine, get_session
from sqlmodel import SQLModel

app = FastAPI()

Optional: for prototyping, you could still do this
SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

### Run server

uvicorn app.main:app --reload

## Important methods / attributes

### SQLModel Class + Attributes

    - class Table(SQLModel, table=True)
    - Field() Properties
        - booleans:
            primary_key, nullable, default(_factory), unique, index
            Index columns that appear in WHERE, JOIN, ORDER BY, or GROUP BY clauses.
        - strs:
            foreign_key('table.id'), ondelete='CASCADE', onupdate='CASCADE'
    - Datetime Properties
        - updated_at: datetime = Field(default_factory=datetime.utcnow)
    - Relationship Properties
        - 1: Many
            - class User(SQLModel, table=True)
                - sessions: list["Session"] = Relationship(back_populates="user")
            - class Session(SQLModel, table=True)
                - user: User | None = Relationship(back_populates='sessions')
                - # User | None is reccommended, because ORM may load object before relationship in populated in memory
        - Many: Many
            - class Program(SQLModel, table=True)
                - exercises: list["Exercise"] = Relationship(
                    back_populates="programs",
                    link_model=ProgramExercise
                    )
            - class Exercise(SQLModel, table=True)
                - programs: list[Program] = Relationship(
                        back_populates="exercises",
                        link_model=ProgramExercise
                    )
            - class ProgramExercise(SQLModel, table=True)
                -   program_id: int = Field(foreign_key="program.id")
                    exercise_id: int = Field(foreign_key="exercise.id")
        - Lazy Loading (N+1 queries)
            -   sessions = session.exec(select(Session)).all()
                for s in sessions:
                    print(s.id)           # no extra queries
                    print(s.created_at)   # no extra queries
                    print(s.user_id)      # no extra queries, just the FK value
                    print(s.user.name)   # triggers a query per session unless eager loaded
            - Eager Load options
                -   select(Session).options(joinedload(Session.user))
                    - SQL LEFT JOIN, stores table in ORM, parents duplicated
                -   select(Session).options(selectinload(Session.user))
                    - Parent + WHERE IN, 1:N, stores parents + children seperately with mapping
                    - Best choice for most cases
                -   select(Session).options(subqueryload(Session.user))
                    - Parent + subquery, RARELY USED

### SQLAlchemy Session

    - Basics
        - session.add(record)
        - session.commit
        - session.refresh(record)
        - with session.begin(): # transaction block: if any transaction fails -> rollback
            - with_for_update()
                # locks row for writing: pessimistic locking
            - session.connection(execution_options={"isolation_level": "SERIALIZABLE"})
                 # READ UNCOMMITTED, READ COMITTED (default), REPEATABLE READ, SERIALIZABLE
        - session.get(Model, id)
    - CRUD
        - Create:
            -  record = Record(name=name, email=email)
        - Read:
            -  record = session.get(Record, record_id)
            -   user = session.exec(select(User).where(User.email == "alice@example.com")).first()
        - Update:
            -   user = session.get(User, user_id)
                if user:
                    user.name = "New Name"
        - Delete:
            -   user = session.get(User, user_id)
                if user:
                    session.delete(user)
                    session.commit()

    - 3 parts of SQLAlchemy Querying
        - EXEC.QUERY.CONSUMER
            - query = select(User).where(User.name == "John")
            - session.exec(query).all()
        - Query
            - Multiple conditions
                - AND
                    - q = select(User).where(User.age >= 18,User.country == "USA")
                - OR
                    - q = select(User).where( or_(User.age < 18, User.country == "Canada"))
                - IN
                    - q = select(User).where(User.id.in_([1, 2, 3]))
                - LIKE
                    - q = select(User).where(User.name.like("%john%"))
            - Sorting/Pagination
                - Order by
                    - q = select(User).order_by(User.created_at.desc())
                - Limit + Offset
                    - q = (select(User).order_by(User.id).offset(20).limit(10))
                - Cursor
                    - q = (select(User).where(User.id > cursor).order_by(User.id).limit(10))
            - JOINS
                - INNER
                    - q = (select(Exercise).join(ProgramExercise, ProgramExercise.exercise_id == Exercise.id).where(ProgramExercise.program_id == program_id))
                - MULTIPLE
                    - q = (select(User, Session).join(Session, Session.user_id == User.id))
                - LEFT
                    - q = (select(Program, ProgramExercise).select_from(outerjoin(Program, ProgramExercise)))
            - AGGREGATORS
                - q = select(func.count(User.id))
                - q = select(func.avg(Session.duration))
            - BULK/BATCH
        - Execute Query
            - result = session.exec(q)
        - Consume Result
            - result.all() # list of rows
            - result.first() # first or None
            - result.one() # exatly one row or error
            - result.scalar() # first column of first row

## Testing

### Pytest

    - Run Tests
        - pytest
    - Asserts
        - assert user.name = 'John'
    - Fixtures
        -   @pytest.fixture
            def sample_user():
                return User(name="John")

            def test_user_name(sample_user):
                assert sample_user.name == "John"
    - Parameterized Tests:
        -   @pytest.mark.parametrize(
                "a,b,expected",
                [
                    (1, 2, 3),
                    (5, 5, 10),
                    (-1, 1, 0),
                ]
            )
            def test_add(a, b, expected):
                assert add(a, b) == expected
    - Test Exceptions
        -   def test_raises():
                with pytest.raises(ValueError):
                    parse_age("not number")
    - Testing FastAPI + SQLModel
        -   from fastapi.testclient import TestClient
            client = TestClient(app)

            def test_home():
                r = client.get("/")
                assert r.status_code == 200

### Coverage
