# Architecture Overview

## High-Level Diagram

```
+-------------------+      +-------------------+      +-------------------+
|  API (FastAPI)    | ---> |  Planner Service  | ---> |  LLM Provider     |
| /plan/sprint      |      | (Validation,      |      | (Ollama/Bedrock)  |
| /llm/model        |      |  Estimation,      |      |                   |
| /health           |      |  Optimization)    |      |                   |
+-------------------+      +-------------------+      +-------------------+
        |                        |                        |
        v                        v                        v
+-------------------+      +-------------------+      +-------------------+
|  Domain Models    |      |  Utils            |      |  Data/Samples     |
| (Employee, Task,  |      | (Skills, Time)    |      | (JSON payloads)   |
+-------------------+      +-------------------+      +-------------------+
```

## Sequence Diagram (Sprint Planning)

1. Client sends POST `/plan/sprint` with JSON payload
2. API validates input, triggers Planner
3. Planner validates, estimates missing effort (calls LLM if needed)
4. Planner runs optimization (PuLP)
5. Planner returns assignments, utilization, summary
6. API responds with plan

## Extensibility
- LLM provider is pluggable (Ollama, Bedrock, future providers)
- Skill taxonomy and mapping can be customized
- Constraints and objectives are configurable

## Security
- JWT authentication for endpoints
- Sensitive data masked in logs
- Rate limiting and request size limits (recommended)

## DevOps
- CI/CD pipeline (lint, test, Docker build)
- Dockerized for local and production use
- Health checks for monitoring
