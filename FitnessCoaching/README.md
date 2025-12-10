# Build a Schema for a Fitness Coaching App

You’re designing the backend for a fitness coaching platform where:

Users can:

Join workout programs

Track their workout sessions

Save progress for each exercise inside a session

Coaches can:

Create workout programs

Add workouts to a program

Add exercises to a workout (e.g., squats, pushups, etc.)

## Schema

### Entities

    Users: name, ..., created_at, updated_at, deleted_at
    Programs: coach_id (FK), progress: %
    Coaches: name, ...
    Session: user_id (FK), program_id(FK)
    Exercises: name,
    Program_Exercises: program_id (FK), execise_id (FK), sets, reps

    Relationships:
        Users:Session = 1:N  (many gets FK)
        Session:Program = N:1  (many gets FK)
        Coaches: Programs: 1: N (many gets FK)
        Programs:Exercse: M: N (new join/relationship table with FKs to each)

        *1:1 Relationships are rare. e.g. Employee:ParkingSpot = 1:1 (FK one one side + unique constraint)

### Models in SQLModel (Pydnatic + SQLAlchemy)

    - Creating a Table  ```python class Table(SQLModel, table=True):```
    - Table Attribute ```python id: int = Field(default=None, primary_key=True)```
    - Foreign Key ```python table_id: int = Field(foreign_key="table.id")```
    - Relationship Table
        ```python class ProgramExercise(SQLModel, table=True):
                    id: int = Field(default=None, primary_key=True)
                    program_id: int = Field(foreign_key="program.id", ondelete="CASCADE")
                    exercise_id: int = Field(foreign_key="exercise.id", ondelete="CASCADE") ```
