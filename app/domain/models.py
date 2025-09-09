from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, conint
from app.domain.enums import Unit, SkillLevel

class Skill(BaseModel):
    name: str
    level: conint(ge=1, le=5)

class SkillRequirement(BaseModel):
    name: str
    min_level: conint(ge=1, le=5)

class Capacity(BaseModel):
    unit: Unit
    available: float = Field(gt=0)
    notes: Optional[str] = None

class Estimate(BaseModel):
    unit: Unit  # "hours" or "points"
    value: float = Field(gt=0)
    confidence: Optional[str] = None  # "high", "medium", "low"
    reasoning: Optional[str] = None

class Team(BaseModel):
    id: str
    name: str
    wip_limit: Optional[int] = None

class Employee(BaseModel):
    id: str
    name: str
    role: str
    team_id: str
    skills: List[Skill]
    capacity: Capacity

class Task(BaseModel):
    id: str
    title: str
    description: str
    required_skills: List[SkillRequirement]
    team_id: Optional[str] = None
    priority: conint(ge=1, le=5)
    estimate: Optional[Estimate] = None
    dependencies: List[str] = Field(default_factory=list)
    max_assignees: int = Field(default=1, ge=1)
    must_have: bool = False

class Sprint(BaseModel):
    id: str
    name: str
    start_date: date
    end_date: date
    timezone: str
    work_days: int
    work_hours_per_day: int
    holidays: List[date] = Field(default_factory=list)
