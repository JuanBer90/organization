from typing import Optional

from app.core.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from sqlmodel import Session, select, col
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse


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


def get_employees(search: str | None, db: Session = Depends(get_db)):
    if search:
        query = select(Employee).where(col(Employee.name).ilike(f"%{search}%"))
    else:
        query = select(Employee)
    return db.exec(query).all()


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