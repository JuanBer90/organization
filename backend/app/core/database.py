from sqlmodel import SQLModel, Session, create_engine
import os

# 📌 Load the database URL from environment variables, defaulting to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../employees.db")

# 📌 Create a database engine
# - `check_same_thread=False` is required for SQLite when using multiple threads
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def init_db():
    """Initializes the database by creating all tables if they do not exist."""
    SQLModel.metadata.create_all(engine)


def get_db():
    """
    Dependency for database session management.
    - Opens a new database session.
    - Yields the session to be used within request handlers.
    - Closes the session automatically when done.
    """
    with Session(engine) as session:
        yield session
