from typing import List

from pydantic import BaseModel, ConfigDict


class EmployeeCreate(BaseModel):
    """
    Schema for creating a new employee.

    - **name**: The name of the employee.
    - **title**: The job title of the employee.

    This schema is used when creating a new employee in the system.
    """
    name: str
    title: str

    # Example of how the data is represented in the API's JSON schema
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Juan Duarte",
            "title": "Software Developer"
        }
    })


class EmployeeCreateResponse(BaseModel):
    """
    Schema for the response returned after creating a new employee.

    - **id**: The unique ID of the newly created employee.
    - **name**: The name of the employee.
    - **title**: The job title of the employee.

    This schema represents the data returned after a successful employee creation.
    """
    id: int
    name: str
    title: str

    # Example representation in the JSON schema
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": 1,
            "name": "Juan Duarte",
            "title": "Software Developer"
        }
    })


class EmployeeUpdate(BaseModel):
    """
    Schema for updating an employee's details.

    - **manager_id**: The ID of the employee's new manager (optional).

    This schema is used for updating an employee's information, specifically their manager.
    """
    manager_id: int | None

    # Example representation in the JSON schema
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "manager_id": 2
        }
    })


class EmployeeResponse(BaseModel):
    """
    Schema for the response returned when fetching an employee's details, including their subordinates.

    - **id**: The unique ID of the employee.
    - **name**: The name of the employee.
    - **title**: The job title of the employee.
    - **employees**: A list of subordinates (employees) under this employee. Currently a placeholder.

    This schema represents the data structure when retrieving employee details.
    """
    id: int
    name: str
    title: str
    employees: List[dict]  # Placeholder for subordinates (list of employee dicts)

    # Example representation in the JSON schema
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": 1,
            "name": "Juan Duarte",
            "title": "Software Developer",
            "employees": []  # Empty list as a placeholder for subordinates
        }
    })
