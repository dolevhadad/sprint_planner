from typing import List, Optional
from pydantic import BaseModel, Field
from app.domain.enums import Unit

class EmployeeAssignment(BaseModel):
    employee_id: str
    unit: Unit
    planned: float = Field(ge=0)

class TaskAssignment(BaseModel):
    task_id: str
    assignees: List[EmployeeAssignment]
    planned_total: float = Field(ge=0)
    team_id: Optional[str] = None

class UnassignedTask(BaseModel):
    task_id: str
    reasons: List[str]
    blocking_dependencies: List[str] = Field(default_factory=list)

class Utilization(BaseModel):
    employee_id: str
    unit: Unit
    planned: float = Field(ge=0)
    capacity: float = Field(gt=0)
    utilization_pct: float = Field(ge=0, le=100)

class PlanSummary(BaseModel):
    total_tasks: int = Field(ge=0)
    assigned_tasks: int = Field(ge=0)
    unassigned_tasks: int = Field(ge=0)
    total_priority_completed: float = Field(ge=0)

class PlanResponse(BaseModel):
    sprint_id: str
    assignments: List[TaskAssignment]
    unassigned: List[UnassignedTask]
    utilization: List[Utilization]
    summary: PlanSummary
    notes: Optional[str] = None
