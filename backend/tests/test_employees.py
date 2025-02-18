import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.core.database import get_db
from app.main import app


# 📌 Fixture: Creates an in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    """
    Sets up an in-memory SQLite database for testing.
    - Uses StaticPool to allow multiple connections in a single thread.
    - Creates all database tables before tests.
    - Provides a database session for the test and closes it afterward.
    """
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


# 📌 Fixture: Creates a test client with an overridden database session
@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Provides a FastAPI test client with a test database session.
    - Overrides the `get_db` dependency to use the in-memory database session.
    - Cleans up dependency overrides after tests.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# 📌 Test: Verify that retrieving employees returns an empty list initially
def test_get_employees_empty(client: TestClient):
    response = client.get("/api/employees")
    assert response.status_code == 200
    assert response.json() == []


# 📌 Test: Create a new employee successfully
def test_create_employee(client: TestClient):
    response = client.post(
        "/api/employees/", json={"name": "Alice", "title": "Designer"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Alice"
    assert data["title"] == "Designer"


# 📌 Test: Attempt to create a duplicate employee (should return an error)
def test_create_duplicate_employee(client: TestClient):
    employee_data = {"name": "Alice", "title": "Designer"}

    # Create the first employee
    client.post("/api/employees", json=employee_data)

    # Try creating the same employee again (should fail)
    response = client.post("/api/employees", json=employee_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "400: An employee with this name already exists"


# 📌 Test: Retrieve employees with a search filter
def test_get_employees_with_search(client: TestClient):
    client.post("/api/employees", json={"name": "Juan", "title": "Developer"})
    client.post("/api/employees", json={"name": "Bob", "title": "Designer"})

    response = client.get("/api/employees?search=juan")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Juan"


# 📌 Test: Assign a manager to an employee successfully
def test_update_manager(client: TestClient):
    emp1 = client.post("/api/employees", json={"name": "Charlie", "title": "Developer"}).json()
    emp2 = client.post("/api/employees", json={"name": "David", "title": "Developer"}).json()

    update_data = {"manager_id": emp1["id"]}
    response = client.put(f"/api/employees/{emp2['id']}/manager", json=update_data)

    assert response.status_code == 200
    assert response.json()["manager_id"] == emp1["id"]


# 📌 Test: Prevent an employee from becoming their own manager
def test_employee_cannot_be_own_manager(client: TestClient):
    emp = client.post("/api/employees", json={"name": "Eve", "title": "Developer"}).json()

    response = client.put(f"/api/employees/{emp['id']}/manager", json={"manager_id": emp["id"]})

    assert response.status_code == 400
    assert response.json()["detail"] == "400: An employee cannot be their own manager"


# 📌 Test: Assigning an invalid manager ID should return an error
def test_update_manager_invalid(client: TestClient):
    emp = client.post("/api/employees", json={"name": "Frank", "title": "Developer"}).json()

    response = client.put(f"/api/employees/{emp['id']}/manager", json={"manager_id": 999})

    assert response.status_code == 400
    assert response.json()["detail"] == "400: Invalid manager_id"
