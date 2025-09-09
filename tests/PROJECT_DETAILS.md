# Project Details: Sprint Planning Assistant

This project is an intelligent sprint planning system powered by LLMs (Language Learning Models) to optimize task assignments and sprint planning for software teams. It considers team member skills, availability, and task requirements to generate optimal sprint plans.

## How It Works

- **Input:**
  - Sprint details (dates, work days, holidays)
  - Teams (IDs, names, WIP limits)
  - Employees (IDs, names, roles, skills, capacity)
  - Tasks (IDs, titles, descriptions, required skills, priority, estimates, dependencies)
  - Planning constraints (max parallel tasks, cross-team assignment, skill match policy, fallback estimation)
  - See `data/samples/sample_plan_request.json` for a full example input.

- **Output:**
  - Task assignments (who does what, how much effort per person)
  - Unassigned tasks (with reasons and blocking dependencies)
  - Employee utilization (planned vs. available capacity)
  - Plan summary (total/assigned/unassigned tasks, priority completed)
  - See the API response schema in `app/schemas/planning_output.py`.

## API Endpoints

- `POST /plan/sprint` — Plan a sprint (see input/output above)
- `GET /health` — Health check

## Example Input
```json
{
  "sprint": { ... },
  "teams": [ ... ],
  "employees": [ ... ],
  "tasks": [ ... ],
  "constraints": { ... }
}
```
See `data/samples/sample_plan_request.json` for a complete example.

## Example Output
```json
{
  "sprint_id": "SPR-2025-09-42",
  "assignments": [ ... ],
  "unassigned": [ ... ],
  "utilization": [ ... ],
  "summary": { ... },
  "notes": "..."
}
```
See `app/schemas/planning_output.py` for details.

## More Information
- For architecture, setup, and usage, see the main [README.md](../README.md).
- For environment variables, see `docs/env_vars.md`.
- For API schema, see `app/schemas/planning_input.py` and `app/schemas/planning_output.py`.
