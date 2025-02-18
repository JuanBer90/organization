from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeUpdate, EmployeeCreate, EmployeeCreateResponse, EmployeeResponse
from app.services import employee_service

router = APIRouter()


@router.post("/employees", response_model=EmployeeCreateResponse,
             summary="Create a new employee",
             description="Adds a new employee to the database. The employee's name must be unique.")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        return employee_service.create_employee(employee, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/employees", response_model=list[EmployeeResponse],
            summary="Retrieve all employees or search by name",
            description="Returns a list of all employees registered in the system. If a search parameter is provided, "
                        "it filters employees by name using a case-insensitive search.")
def get_employees(search: str = None, db: Session = Depends(get_db)):
    # TODO: If there are too many employees, consider adding pagination to improve performance.
    try:
        return employee_service.get_employees(search, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/employees/{employee_id}", status_code=204, summary="Delete an employee",
               description="Deletes an employee only if they do not have subordinates. "
                           "If the employee has subordinates, reassign or remove them before deleting.")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    try:
        return employee_service.delete_employee(employee_id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/employees/{employee_id}/manager",
            response_model=Employee,
            summary="Update employee manager",
            description="Updates the manager of a given employee. An employee cannot be their own manager.")
def update_manager(employee_id: int, update: EmployeeUpdate, db: Session = Depends(get_db)):
    try:
        return employee_service.update_manager(employee_id, update, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))