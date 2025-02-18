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
