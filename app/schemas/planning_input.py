from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.domain.models import Sprint, Team, Employee, Task
from app.domain.enums import MatchPolicy, Objective, Unit

class FallbackEstimation(BaseModel):
    enabled: bool = True
    unit: Unit
    default_value: float = Field(gt=0)

class Constraints(BaseModel):
    max_parallel_tasks_per_person: int = Field(default=2, ge=1)
    allow_cross_team: bool = False
    match_policy: MatchPolicy = MatchPolicy.THRESHOLD
    min_skill_level_match: int = Field(default=0, ge=0, le=2)
    objective: Objective = Objective.MAXIMIZE_PRIORITY
    fallback_estimation: Optional[FallbackEstimation] = None

class PlanRequest(BaseModel):
    sprint: Sprint
    teams: List[Team]
    employees: List[Employee]
    tasks: List[Task]
    constraints: Optional[Constraints] = None
