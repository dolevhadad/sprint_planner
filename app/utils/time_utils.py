from datetime import datetime, timedelta
from typing import List, Optional
from zoneinfo import ZoneInfo

def calculate_work_hours(
    start_date: datetime,
    end_date: datetime,
    work_hours_per_day: int,
    holidays: Optional[List[datetime]] = None,
    timezone: str = "UTC"
) -> float:
    """Calculate total work hours between dates, excluding weekends and holidays."""
    
    tz = ZoneInfo(timezone)
    start = start_date.replace(tzinfo=tz)
    end = end_date.replace(tzinfo=tz)
    holidays = holidays or []
    
    total_hours = 0
    current = start
    
    while current <= end:
        # Skip weekends (5 = Saturday, 6 = Sunday)
        if current.weekday() < 5:
            # Skip holidays
            if current.date() not in [h.date() for h in holidays]:
                total_hours += work_hours_per_day
        current += timedelta(days=1)
    
    return total_hours

def normalize_skill_name(skill: str) -> str:
    """Normalize skill names for consistent matching."""
    
    # Common abbreviations and variations
    mappings = {
        "js": "javascript",
        "ts": "typescript",
        "py": "python",
        "react.js": "react",
        "react-js": "react",
        "node.js": "nodejs",
        "node-js": "nodejs",
        "vue.js": "vue",
        "vue-js": "vue",
        "postgres": "postgresql",
        "k8s": "kubernetes",
        "aws-lambda": "lambda",
        "dl": "deep-learning",
        "ml": "machine-learning",
        "ai": "artificial-intelligence",
        "ui": "user-interface",
        "ux": "user-experience",
    }
    
    normalized = skill.lower().strip()
    return mappings.get(normalized, normalized)
