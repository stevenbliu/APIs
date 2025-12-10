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
    Programs: coach_id (FK)
    Coaches: name, ...
    Session: user_id (FK), program_id(FK), progress, exercises_completed, total_exercises
    Exercises: name, category (chest)
    Program_Exercises: program_id (FK), exercise_id (FK), sets, reps
    Program_User: program_id (FK), user_id (FK)
    Session_Exercise: session_id, exercise_id, current_set, current_rep, completed

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

### Standard Queries

    - Get/Create Programs
        - session.get(Program, id)
        - session.add(Program)
    - Add Exercise to Programs
        - Add exercise_id, program_id, reps, sets to ExercisePrograms Table
            - new_ExerciseProgram = ExerciseProgram(exercise_id, program_id, reps, sets)
            - session.add(new_ExerciseProgram)
    - Add Workout to Exercise
        - session.add(Exercise)
    - Users can join programs
        - Search for programs with offset
            - query = select(Programs).where(zip_code=...).order_by(date).offset(20).limit(10)
        - Search for programs with cursor
            - query = select(Programs).where(zip_code=..., id>cursor).order_by(id).offset(20).limit(10)
        -  return session.exec(query).all()
        - Add program_id, user_id to UserPrograms Table
            - new_UserProgram = UserProgram(program_id, user_id, ...)
            - session.add(new_UserProgram)
    - View Current Session of User
        - query = select(Session).where(Session.user_id == user_id, Session.active=True)
        - return session.exec(query).first()
