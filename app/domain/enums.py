from enum import Enum
from typing import Optional

class SkillLevel(int, Enum):
    NOVICE = 1
    BEGINNER = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5

class Priority(int, Enum):
    LOW = 1
    MEDIUM_LOW = 2
    MEDIUM = 3
    MEDIUM_HIGH = 4
    HIGH = 5

class Unit(str, Enum):
    HOURS = "hours"
    POINTS = "points"

class Objective(str, Enum):
    MAXIMIZE_PRIORITY = "maximize_priority_completed"
    BALANCE_UTILIZATION = "balance_utilization"

class MatchPolicy(str, Enum):
    THRESHOLD = "threshold"
    WEIGHTED = "weighted"
