
from typing import List
from app.domain.models import Task
from app.llm.base import LLMClient
from app.llm.ollama_provider import OllamaProvider
from app.llm.bedrock_provider import BedrockProvider
from app.core.config import get_settings
from app.utils.llm_cache import llm_cache

settings = get_settings()

class TaskEstimator:
    def __init__(self):
        self.llm_client = self._get_llm_client()

    def _get_llm_client(self) -> LLMClient:
        """Get the configured LLM client."""
        if settings.MODEL_PROVIDER == "ollama":
            return OllamaProvider()
        elif settings.MODEL_PROVIDER == "bedrock":
            return BedrockProvider()
        else:
            raise ValueError(f"Unsupported model provider: {settings.MODEL_PROVIDER}")

    async def estimate_tasks(self, tasks: List[Task]) -> List[Task]:
        """Estimate effort for tasks without estimates, with caching."""
        updated_tasks = []
        for task in tasks:
            if task.estimate is None:
                estimate = await self._estimate_single_task(task)
                updated_tasks.append(Task(
                    **{**task.model_dump(), "estimate": estimate}
                ))
            else:
                updated_tasks.append(task)
        return updated_tasks

    async def _estimate_single_task(self, task: Task) -> dict:
        """Get estimate for a single task using LLM, with cache and fallback."""
        skill_names = [s.name for s in task.required_skills]
        cache_key_params = {
            "description": task.description,
            "skills": skill_names,
            "provider": settings.MODEL_PROVIDER,
            "model": settings.OLLAMA_MODEL if settings.MODEL_PROVIDER == "ollama" else settings.BEDROCK_MODEL
        }
        cached = llm_cache.get("estimate_task", cache_key_params)
        if cached:
            return cached
        try:
            response = await self.llm_client.estimate_task(
                task_description=task.description,
                required_skills=skill_names
            )
            # Log the raw LLM response for debugging
            import logging
            logging.getLogger("estimator").info(f"Raw LLM response: {response}")
            if not isinstance(response, dict) or "unit" not in response or "value" not in response:
                logging.getLogger("estimator").warning(f"LLM response missing required fields, using fallback. Response: {response}")
                if hasattr(settings, "DEFAULT_TASK_ESTIMATE"):
                    return {
                        "unit": "hours",
                        "value": settings.DEFAULT_TASK_ESTIMATE
                    }
                else:
                    return {
                        "unit": "hours",
                        "value": 8
                    }
            llm_cache.set("estimate_task", cache_key_params, response)
            return response
        except Exception as e:
            logging.getLogger("estimator").error(f"LLM estimation failed, using fallback. Error: {e}")
            if hasattr(settings, "DEFAULT_TASK_ESTIMATE"):
                return {
                    "unit": "hours",
                    "value": settings.DEFAULT_TASK_ESTIMATE
                }
            else:
                return {
                    "unit": "hours",
                    "value": 8
                }
