from typing import Dict, List, Optional, Tuple
import pulp
from app.domain.models import Employee, Task, Sprint
from app.schemas.planning_input import PlanRequest, Constraints
from app.schemas.planning_output import (
    PlanResponse, TaskAssignment, EmployeeAssignment,
    UnassignedTask, Utilization, PlanSummary
)
from app.core.logging import log_event, log_error
from app.services.validator import PlanValidator
from app.services.estimator import TaskEstimator

class SprintPlanner:
    def __init__(self):
        self.validator = PlanValidator()
        self.estimator = TaskEstimator()

    async def create_plan(self, request: PlanRequest) -> PlanResponse:
        """Create a sprint plan based on the request."""
        
        # Validate inputs
        self.validator.validate_request(request)
        
        # Estimate any tasks without estimates
        tasks = await self._ensure_task_estimates(request.tasks)
        
        # Create and solve the optimization problem
        assignments = self._optimize_assignments(
            tasks=tasks,
            employees=request.employees,
            sprint=request.sprint,
            constraints=request.constraints or Constraints()
        )
        
        # Calculate utilization and unassigned tasks
        utilization = self._calculate_utilization(
            assignments=assignments,
            employees=request.employees,
            sprint=request.sprint
        )
        
        unassigned = self._get_unassigned_tasks(
            assignments=assignments,
            tasks=tasks
        )
        
        # Create summary
        summary = self._create_summary(
            assignments=assignments,
            unassigned=unassigned,
            tasks=tasks
        )
        
        return PlanResponse(
            sprint_id=request.sprint.id,
            assignments=assignments,
            unassigned=unassigned,
            utilization=utilization,
            summary=summary
        )

    async def _ensure_task_estimates(self, tasks: List[Task]) -> List[Task]:
        """Ensure all tasks have estimates."""
        return await self.estimator.estimate_tasks(tasks)

    def _optimize_assignments(
        self,
        tasks: List[Task],
        employees: List[Employee],
        sprint: Sprint,
        constraints: Constraints
    ) -> List[TaskAssignment]:
        """Optimize task assignments using PuLP. Always report unassigned tasks if infeasible."""
        # Create the optimization problem
        prob = pulp.LpProblem("SprintPlanning", pulp.LpMaximize)
        # Decision variables: x[i,j] = 1 if employee i is assigned to task j
        x = pulp.LpVariable.dicts(
            "assign",
            ((e.id, t.id) for e in employees for t in tasks),
            cat='Binary'
        )
        # Objective: Maximize priority * completion
        prob += pulp.lpSum(
            t.priority * x[e.id, t.id]
            for e in employees
            for t in tasks
        )
        # Constraints
        self._add_capacity_constraints(prob, x, tasks, employees, sprint)
        self._add_skill_constraints(prob, x, tasks, employees, constraints)
        self._add_assignment_constraints(prob, x, tasks, employees, constraints)
        # Solve
        prob.solve()
        # If infeasible, return no assignments (all tasks will be unassigned)
        if pulp.LpStatus[prob.status] == "Infeasible":
            return []
        # Convert solution to assignments
        return self._convert_solution_to_assignments(x, tasks, employees)

    def _add_capacity_constraints(
        self,
        prob: pulp.LpProblem,
        x: Dict,
        tasks: List[Task],
        employees: List[Employee],
        sprint: Sprint
    ) -> None:
        """Add capacity constraints to the optimization problem."""
        for e in employees:
            prob += pulp.lpSum(
                t.estimate.value * x[e.id, t.id]
                for t in tasks
                if t.estimate
            ) <= e.capacity.available

    def _add_skill_constraints(
        self,
        prob: pulp.LpProblem,
        x: Dict,
        tasks: List[Task],
        employees: List[Employee],
        constraints: Constraints
    ) -> None:
        """Add skill matching constraints."""
        for t in tasks:
            for skill_req in t.required_skills:
                prob += pulp.lpSum(
                    x[e.id, t.id]
                    for e in employees
                    if any(
                        s.name == skill_req.name and 
                        s.level >= skill_req.min_level - constraints.min_skill_level_match
                        for s in e.skills
                    )
                ) >= 1

    def _add_assignment_constraints(
        self,
        prob: pulp.LpProblem,
        x: Dict,
        tasks: List[Task],
        employees: List[Employee],
        constraints: Constraints
    ) -> None:
        """Add assignment constraints."""
        # Max assignees per task
        for t in tasks:
            prob += pulp.lpSum(x[e.id, t.id] for e in employees) <= t.max_assignees
        
        # Max parallel tasks per person
        for e in employees:
            prob += pulp.lpSum(x[e.id, t.id] for t in tasks) <= constraints.max_parallel_tasks_per_person

    def _convert_solution_to_assignments(
        self,
        x: Dict,
        tasks: List[Task],
        employees: List[Employee]
    ) -> List[TaskAssignment]:
        """Convert optimization solution to TaskAssignments."""
        assignments = []
        for t in tasks:
            assignees = []
            for e in employees:
                if pulp.value(x[e.id, t.id]) == 1:
                    assignees.append(e)
            num_assignees = len(assignees)
            if num_assignees > 0:
                split_effort = t.estimate.value / num_assignees if num_assignees else 0.0
                assignment_objs = [
                    EmployeeAssignment(
                        employee_id=a.id,
                        unit=t.estimate.unit,
                        planned=split_effort
                    ) for a in assignees
                ]
                assignments.append(TaskAssignment(
                    task_id=t.id,
                    assignees=assignment_objs,
                    planned_total=t.estimate.value,
                    team_id=t.team_id
                ))
        return assignments

    def _calculate_utilization(
        self,
        assignments: List[TaskAssignment],
        employees: List[Employee],
        sprint: Sprint
    ) -> List[Utilization]:
        """Calculate utilization per employee, guarding against division by zero."""
        utilization = []
        for e in employees:
            planned = sum(
                a.planned
                for t in assignments
                for a in t.assignees
                if a.employee_id == e.id
            )
            capacity = getattr(e.capacity, "available", 0)
            if not capacity or capacity <= 0:
                pct = 0.0
            else:
                pct = round((planned / capacity) * 100, 1)
                if pct > 100:
                    pct = 100.0
            utilization.append(Utilization(
                employee_id=e.id,
                unit=e.capacity.unit,
                planned=planned,
                capacity=capacity,
                utilization_pct=pct
            ))
        return utilization

    def _get_unassigned_tasks(
        self,
        assignments: List[TaskAssignment],
        tasks: List[Task]
    ) -> List[UnassignedTask]:
        """Get list of unassigned tasks with reasons."""
        assigned_ids = {a.task_id for a in assignments}
        unassigned = []
        for t in tasks:
            if t.id not in assigned_ids:
                # Simple reasons for now - expand based on constraint analysis
                reasons = ["Insufficient capacity or skill match"]
                if t.dependencies:
                    reasons.append("Has dependencies")
                unassigned.append(UnassignedTask(
                    task_id=t.id,
                    reasons=reasons,
                    blocking_dependencies=t.dependencies
                ))
        return unassigned

    def _create_summary(
        self,
        assignments: List[TaskAssignment],
        unassigned: List[UnassignedTask],
        tasks: List[Task]
    ) -> PlanSummary:
        """Create plan summary statistics."""
        return PlanSummary(
            total_tasks=len(tasks),
            assigned_tasks=len(assignments),
            unassigned_tasks=len(unassigned),
            total_priority_completed=sum(
                t.priority
                for t in tasks
                if t.id in {a.task_id for a in assignments}
            )
        )
