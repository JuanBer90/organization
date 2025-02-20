from typing import List
from typing import Optional

from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, col

from app.core.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse


def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    # Query to check if an employee with the same name already exists
    query = select(Employee).where(Employee.name.ilike(employee.name))

    # Check if the employee already exists
    existing_employee = db.exec(query).first()

    if existing_employee:
        raise HTTPException(status_code=400, detail="An employee with this name already exists")

    # Create a new employee instance with the provided name and title
    new_employee = Employee(name=employee.name, title=employee.title)  # Only assign name and title

    # Add the new employee to the session and commit the transaction
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


def get_employees(search: str | None = None, db: Session = Depends(get_db)) -> List[EmployeeResponse]:
    """Fetches all employees and organizes them into a nested manager-subordinate structure."""

    # Select all employees with an optional search filter
    query = select(Employee)
    if search:
        query = query.where(col(Employee.name).ilike(f"%{search}%"))

    employees = db.exec(query).all()

    # Create a dictionary to store managers and their subordinates
    managers_dict = {}

    # Identify managers and initialize their structure
    for emp in employees:
        if emp.manager_id is None:
            managers_dict[emp.id] = {
                "name": emp.name,
                "title": emp.title,
                "id": emp.id,
                "employees": []  # Placeholder for subordinates
            }

    # Assign employees to their respective managers
    for emp in employees:
        if emp.manager_id is not None and emp.manager_id in managers_dict:
            managers_dict[emp.manager_id]["employees"].append({
                "name": emp.name,
                "title": emp.title,
                "id": emp.id,
            })

    # Convert the manager dictionary into a list of EmployeeResponse models
    employee_responses = [
        EmployeeResponse(
            id=manager["id"],
            name=manager["name"],
            title=manager["title"],
            employees=manager["employees"]
        ) for manager in managers_dict.values()
    ]

    return employee_responses


def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    # Retrieve the employee by ID
    employee = db.get(Employee, employee_id)

    # If employee is not found, raise a 404 error
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check if the employee has subordinates before deleting
    subordinates = db.exec(select(Employee).where(Employee.manager_id == employee_id)).first()
    if subordinates:
        raise HTTPException(status_code=400,
                            detail="Cannot delete employee with assigned subordinates. Reassign or remove "
                                   "subordinates first.")

    # Delete the employee from the database and commit the transaction
    db.delete(employee)
    db.commit()

    return dict(status_code=204, content={"message": "Employee deleted successfully"})


def update_manager(employee_id: int, update: EmployeeUpdate, db: Session = Depends(get_db)):
    # Retrieve the employee by ID
    employee: Optional[Employee] = db.get(Employee, employee_id)

    # If employee is not found, raise a 404 error
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Prevent an employee from being their own manager
    if update.manager_id == employee_id:
        raise HTTPException(status_code=400, detail="An employee cannot be their own manager")

    # Retrieve the new manager and validate the manager ID
    manager = db.get(Employee, update.manager_id)

    if update.manager_id and not manager:
        raise HTTPException(status_code=400, detail="Invalid manager_id")

    # Update the employee's manager ID and commit the changes
    employee.manager_id = update.manager_id
    db.commit()
    db.refresh(employee)

    return employee
