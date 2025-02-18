from fastapi import FastAPI
from app.api.routes import employees
from contextlib import asynccontextmanager
from app.core.database import init_db  # Import the function


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Initialize database at startup
    yield  # Execution continues here after startup


app = FastAPI(title="Organization Chart API",
              description="A FastAPI-based backend for managing an organization chart,"
                          " allowing employee management and hierarchical structure updates.",
              lifespan=lifespan)
app.include_router(employees.router, prefix="/api", tags=["employees"])
