from typing import List, Dict, Any
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, col

from app.core.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse


def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    query = select(Employee).where(Employee.name.ilike(employee.name))

    existing_employee = db.exec(query).first()

    if existing_employee:
        raise HTTPException(status_code=400, detail="An employee with this name already exists")

    new_employee = Employee(name=employee.name, title=employee.title)  # Only assign name and title

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


from sqlmodel import Session, select, col
from fastapi import Depends
from typing import List, Dict, Any


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

    print(managers_dict)
    # Return only the list of managers (not wrapped in a dictionary)
    # Convert each manager's dictionary to an EmployeeResponse model
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
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    subordinates = db.exec(select(Employee).where(Employee.manager_id == employee_id)).first()
    if subordinates:
        raise HTTPException(status_code=400,
                            detail="Cannot delete employee with assigned subordinates. Reassign or remove "
                                   "subordinates first.")

    db.delete(employee)
    db.commit()
    return JSONResponse(status_code=404, content={"message": "Employee deleted successfully"})


def update_manager(employee_id: int, update: EmployeeUpdate, db: Session = Depends(get_db)):
    employee: Optional[Employee] = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if update.manager_id == employee_id:
        raise HTTPException(status_code=400, detail="An employee cannot be their own manager")

    manager = db.get(Employee, update.manager_id)

    if update.manager_id and not manager:
        raise HTTPException(status_code=400, detail="Invalid manager_id")

    employee.manager_id = update.manager_id
    db.commit()
    db.refresh(employee)

    return employee