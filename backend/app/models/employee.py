from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


# 📌 Employee model representing an employee in the database
class Employee(SQLModel, table=True):
    """
    Employee model representing an employee in the organization.
    - Stores basic employee details such as name and title.
    - Supports hierarchical relationships (an employee can have a manager).
    """

    # Unique identifier for each employee (Primary Key)
    id: Optional[int] = Field(default=None, primary_key=True)

    # Employee's name (must be unique and cannot be null)
    name: str = Field(index=True, unique=True, nullable=False)

    # Employee's job title (cannot be null)
    title: str = Field(nullable=False)

    # Manager ID references another employee (Foreign Key)
    manager_id: int | None = Field(default=None, foreign_key="employee.id")

    # Relationship to define an employee's manager (self-referencing relationship)
    manager: Optional["Employee"] = Relationship()

    # Configuration settings for the model
    model_config = {
        "from_attributes": True,  # Allows creating objects from database records
        "validate_assignment": True  # Enables validation when updating attributes
    }
