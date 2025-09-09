def weighted_skill_match(
    required_level: int,
    actual_level: int,
    policy: str = "threshold"
) -> float:
    """
    Calculate skill match score between required and actual levels.
    
    Args:
        required_level: Required skill level (1-5)
        actual_level: Actual skill level (1-5)
        policy: "threshold" or "weighted"
    
    Returns:
        Match score between 0 and 1
    """
    if policy == "threshold":
        return 1.0 if actual_level >= required_level else 0.0
    
    # Weighted scoring
    if actual_level >= required_level:
        return 1.0
    
    # Partial credit for near matches
    diff = required_level - actual_level
    if diff == 1:
        return 0.75
    elif diff == 2:
        return 0.5
    else:
        return 0.0

def calculate_team_coverage(
    required_skills: list[dict],
    team_skills: list[dict]
) -> dict:
    """
    Calculate skill coverage for a team.
    
    Args:
        required_skills: List of {"name": str, "min_level": int}
        team_skills: List of {"name": str, "level": int}
    
    Returns:
        Dict with coverage metrics
    """
    coverage = {}
    
    for req in required_skills:
        skill_name = req["name"]
        required_level = req["min_level"]
        
        # Find team members with this skill
        matches = [
            s["level"] for s in team_skills 
            if s["name"] == skill_name
        ]
        
        if matches:
            max_level = max(matches)
            coverage[skill_name] = {
                "required": required_level,
                "available": max_level,
                "covered": max_level >= required_level,
                "team_members": len(matches)
            }
        else:
            coverage[skill_name] = {
                "required": required_level,
                "available": 0,
                "covered": False,
                "team_members": 0
            }
    
    return {
        "skills": coverage,
        "fully_covered": all(s["covered"] for s in coverage.values()),
        "coverage_ratio": sum(1 for s in coverage.values() if s["covered"]) / len(coverage)
    }
