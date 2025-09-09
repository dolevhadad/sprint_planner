from typing import List
from app.domain.models import Task, Employee, Team
from app.schemas.planning_input import PlanRequest
from app.core.logging import log_error

class PlanValidator:
    def validate_request(self, request: PlanRequest) -> None:
        """Validate the planning request."""
        self._validate_dates(request)
        self._validate_teams(request.teams)
        self._validate_employees(request.employees, request.teams)
        self._validate_tasks(request.tasks, request.teams)
        self._validate_dependencies(request.tasks)

    def _validate_dates(self, request: PlanRequest) -> None:
        """Validate sprint dates."""
        if request.sprint.end_date <= request.sprint.start_date:
            raise ValueError("Sprint end date must be after start date")
        
        if any(h < request.sprint.start_date or h > request.sprint.end_date 
               for h in request.sprint.holidays):
            raise ValueError("Holidays must be within sprint dates")

    def _validate_teams(self, teams: List[Team]) -> None:
        """Validate team data."""
        team_ids = set()
        for team in teams:
            if team.id in team_ids:
                raise ValueError(f"Duplicate team ID: {team.id}")
            team_ids.add(team.id)
            
            if team.wip_limit is not None and team.wip_limit < 1:
                raise ValueError(f"Invalid WIP limit for team {team.id}")

    def _validate_employees(self, employees: List[Employee], teams: List[Team]) -> None:
        """Validate employee data."""
        employee_ids = set()
        team_ids = {t.id for t in teams}
        
        for emp in employees:
            if emp.id in employee_ids:
                raise ValueError(f"Duplicate employee ID: {emp.id}")
            employee_ids.add(emp.id)
            
            if emp.team_id not in team_ids:
                raise ValueError(f"Invalid team ID {emp.team_id} for employee {emp.id}")
            
            if not emp.skills:
                raise ValueError(f"Employee {emp.id} has no skills")
            
            if emp.capacity.available <= 0:
                raise ValueError(f"Invalid capacity for employee {emp.id}")

    def _validate_tasks(self, tasks: List[Task], teams: List[Team]) -> None:
        """Validate task data."""
        task_ids = set()
        team_ids = {t.id for t in teams}
        
        for task in tasks:
            if task.id in task_ids:
                raise ValueError(f"Duplicate task ID: {task.id}")
            task_ids.add(task.id)
            
            if task.team_id and task.team_id not in team_ids:
                raise ValueError(f"Invalid team ID {task.team_id} for task {task.id}")
            
            if not task.required_skills:
                raise ValueError(f"Task {task.id} has no required skills")
            
            if task.estimate and task.estimate.value <= 0:
                raise ValueError(f"Invalid estimate for task {task.id}")
            
            if task.max_assignees < 1:
                raise ValueError(f"Invalid max_assignees for task {task.id}")

    def _validate_dependencies(self, tasks: List[Task]) -> None:
        """Validate task dependencies."""
        task_ids = {t.id for t in tasks}
        
        for task in tasks:
            for dep_id in task.dependencies:
                if dep_id not in task_ids:
                    raise ValueError(f"Invalid dependency {dep_id} for task {task.id}")
            
            # Check for cycles
            visited = set()
            self._check_dependency_cycle(task.id, task.dependencies, tasks, visited)

    def _check_dependency_cycle(
        self,
        task_id: str,
        dependencies: List[str],
        tasks: List[Task],
        visited: set
    ) -> None:
        """Check for dependency cycles using DFS."""
        if task_id in visited:
            raise ValueError(f"Dependency cycle detected involving task {task_id}")
        
        visited.add(task_id)
        
        for dep_id in dependencies:
            dep_task = next((t for t in tasks if t.id == dep_id), None)
            if dep_task:
                self._check_dependency_cycle(dep_task.id, dep_task.dependencies, tasks, visited.copy())
