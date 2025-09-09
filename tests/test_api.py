import pytest
from fastapi.testclient import TestClient
from app.api.routes import app

@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)

def test_health(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.parametrize(
    "payload,expected_keys",
    [
        (
            {
                "sprint": {
                    "id": "SPR-2025-09-42",
                    "name": "Sprint 42",
                    "start_date": "2025-09-15",
                    "end_date": "2025-09-29",
                    "timezone": "UTC",
                    "work_days": 10,
                    "work_hours_per_day": 8
                },
                "teams": [
                    {"id": "TEAM-PLAT", "name": "Platform", "wip_limit": 10},
                    {"id": "TEAM-WEB", "name": "Web", "wip_limit": 8}
                ],
                "employees": [
                    {
                        "id": "E1",
                        "name": "Ari Cohen",
                        "role": "Backend Engineer",
                        "team_id": "TEAM-PLAT",
                        "skills": [
                            {"name": "python", "level": 4},
                            {"name": "aws", "level": 3},
                            {"name": "sql", "level": 4}
                        ],
                        "capacity": {"unit": "hours", "available": 64}
                    }
                ],
                "tasks": [
                    {
                        "id": "T-101",
                        "title": "User session service",
                        "description": "Build stateless session service with JWT and Redis.",
                        "required_skills": [
                            {"name": "python", "min_level": 3},
                            {"name": "aws", "min_level": 2}
                        ],
                        "team_id": "TEAM-PLAT",
                        "priority": 5,
                        "estimate": {"unit": "hours", "value": 24},
                        "dependencies": [],
                        "max_assignees": 2,
                        "must_have": True
                    }
                ],
                "constraints": {
                    "max_parallel_tasks_per_person": 2,
                    "allow_cross_team": False
                }
            },
            ["assignments", "summary"]
        ),
        (
            {
                "sprint": {
                    "id": "SPR-2025-09-42",
                    "name": "Sprint 42",
                    "start_date": "2025-09-15",
                    "end_date": "2025-09-29",
                    "timezone": "UTC",
                    "work_days": 10,
                    "work_hours_per_day": 8
                },
                "teams": [
                    {"id": "TEAM-PLAT", "name": "Platform", "wip_limit": 10},
                    {"id": "TEAM-WEB", "name": "Web", "wip_limit": 8}
                ],
                "employees": [
                    {
                        "id": "E1",
                        "name": "Ari Cohen",
                        "role": "Backend Engineer",
                        "team_id": "TEAM-PLAT",
                        "skills": [
                            {"name": "python", "level": 4},
                            {"name": "aws", "level": 3},
                            {"name": "sql", "level": 4}
                        ],
                        "capacity": {"unit": "hours", "available": 10}
                    }
                ],
                "tasks": [
                    {
                        "id": "T-101",
                        "title": "Big task",
                        "description": "Impossible workload.",
                        "required_skills": [
                            {"name": "python", "min_level": 3}
                        ],
                        "team_id": "TEAM-PLAT",
                        "priority": 5,
                        "estimate": {"unit": "hours", "value": 100},
                        "dependencies": [],
                        "max_assignees": 1,
                        "must_have": True
                    }
                ],
                "constraints": {
                    "max_parallel_tasks_per_person": 1,
                    "allow_cross_team": False
                }
            },
            ["unassigned"]
        ),
    ]
)
def test_plan_sprint_scenarios(test_client, payload, expected_keys):
    response = test_client.post("/plan/sprint", json=payload)
    assert response.status_code == 200
    for key in expected_keys:
        assert key in response.json()

def test_plan_sprint_optional_task(test_client):
    # Optional task scenario
    payload = {
        "sprint": {
            "id": "SPR-2025-09-42",
            "name": "Sprint 42",
            "start_date": "2025-09-15",
            "end_date": "2025-09-29",
            "timezone": "UTC",
            "work_days": 10,
            "work_hours_per_day": 8
        },
        "teams": [
            {"id": "TEAM-PLAT", "name": "Platform", "wip_limit": 10}
        ],
        "employees": [
            {
                "id": "E1",
                "name": "Ari Cohen",
                "role": "Backend Engineer",
                "team_id": "TEAM-PLAT",
                "skills": [
                    {"name": "python", "level": 4}
                ],
                "capacity": {"unit": "hours", "available": 8}
            }
        ],
        "tasks": [
            {
                "id": "T-101",
                "title": "Must have",
                "description": "Required task.",
                "required_skills": [
                    {"name": "python", "min_level": 3}
                ],
                "team_id": "TEAM-PLAT",
                "priority": 5,
                "estimate": {"unit": "hours", "value": 8},
                "dependencies": [],
                "max_assignees": 1,
                "must_have": True
            },
            {
                "id": "T-102",
                "title": "Maybe",
                "description": "Optional task.",
                "required_skills": [
                    {"name": "python", "min_level": 3}
                ],
                "team_id": "TEAM-PLAT",
                "priority": 1,
                "estimate": {"unit": "hours", "value": 8},
                "dependencies": [],
                "max_assignees": 1,
                "must_have": False
            }
        ],
        "constraints": {
            "max_parallel_tasks_per_person": 1,
            "allow_cross_team": False
        }
    }
    response = test_client.post("/plan/sprint", json=payload)
    assert response.status_code == 200
    assert "assignments" in response.json()
    assert "unassigned" in response.json()
    # Optional task should be unassigned if capacity is insufficient
    assert any(t["task_id"] == "T-102" for t in response.json()["unassigned"])
    # End of valid test suite. All code below this line has been removed.
