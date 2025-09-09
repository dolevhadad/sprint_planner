from fastapi import FastAPI, HTTPException, status, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from app.schemas.planning_input import PlanRequest
from app.schemas.planning_output import PlanResponse
from app.services.planner import SprintPlanner
from app.core.logging import log_error
from app.core.config import get_settings

app = FastAPI(
    title="Sprint Planning API",
    description="LLM-powered sprint planning and optimization.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Planning", "description": "Sprint planning endpoints."},
        {"name": "Health", "description": "Health check endpoint."}
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2/JWT security (placeholder)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@app.post("/llm/model", tags=["Planning"], summary="Set LLM model", response_description="Model updated")
async def set_llm_model(
    provider: str = Body(..., embed=True, example="ollama"),
    model: str = Body(..., embed=True, example="llama2")
):
    """Set the LLM provider and model (Ollama or Bedrock)."""
    settings = get_settings()
    settings.MODEL_PROVIDER = provider
    if provider == "ollama":
        settings.OLLAMA_MODEL = model
    elif provider == "bedrock":
        settings.BEDROCK_MODEL = model
    else:
        raise HTTPException(status_code=400, detail="Unknown provider")
    return {"provider": provider, "model": model}

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from app.schemas.planning_input import PlanRequest
from app.schemas.planning_output import PlanResponse
from app.services.planner import SprintPlanner
from app.core.logging import log_error

app = FastAPI(
    title="Sprint Planning API",
    description="LLM-powered sprint planning and optimization.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Planning", "description": "Sprint planning endpoints."},
        {"name": "Health", "description": "Health check endpoint."}
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2/JWT security (placeholder)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@app.get("/health", tags=["Health"], summary="Health check", response_description="API health status")
async def health_check():
    """Check API health."""
    return {"status": "healthy"}

@app.post(
    "/plan/sprint",
    response_model=PlanResponse,
    tags=["Planning"],
    summary="Plan a sprint",
    response_description="Sprint plan assignments and utilization",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Sprint plan generated successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "sprint_id": "SPR-2025-09-42",
                        "assignments": [
                            {"task_id": "T-101", "assignees": [{"employee_id": "E1", "unit": "hours", "planned": 12}], "planned_total": 24, "team_id": "TEAM-PLAT"}
                        ],
                        "unassigned": [
                            {"task_id": "T-102", "reasons": ["Insufficient capacity or skill match"], "blocking_dependencies": ["T-101"]}
                        ],
                        "utilization": [
                            {"employee_id": "E1", "unit": "hours", "planned": 12, "capacity": 64, "utilization_pct": 18.75}
                        ],
                        "summary": {
                            "total_tasks": 3,
                            "assigned_tasks": 2,
                            "unassigned_tasks": 1,
                            "total_priority_completed": 9
                        },
                        "notes": "Sprint plan generated."
                    }
                }
            }
        },
        400: {"description": "Validation error."},
        401: {"description": "Unauthorized."},
        500: {"description": "Internal server error."}
    }
)
async def plan_sprint(request: PlanRequest, token: str = Depends(oauth2_scheme) if get_settings().AUTH_ENABLED else None):
    """Generate a sprint plan based on input data."""
    try:
        planner = SprintPlanner()
        response = await planner.create_plan(request)
        return response
    except ValueError as ve:
        log_error(ve, {"request": request.model_dump()})
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        log_error(e, {"request": request.model_dump()})
        raise HTTPException(status_code=500, detail="Internal error: " + str(e))
