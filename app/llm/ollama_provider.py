import httpx
import json
import logging
from typing import Dict, Any, Optional, List
from app.llm.base import LLMClient
from app.core.config import get_settings
try:
    from app.core.logging import logger as custom_logger
except ImportError:
    custom_logger = None

settings = get_settings()

class OllamaProvider(LLMClient):
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.client = httpx.AsyncClient(timeout=60.0)

    async def chat(self, messages: list, json_mode: bool = False, tools: list = None) -> str:
        # Stub implementation for compatibility
        return "Ollama chat not implemented."

    async def estimate_task(self, task_description: str, required_skills: list = None) -> dict:
        # Use the existing sync estimate_task logic for now
        return self._estimate_task_sync(task_description)

    def _estimate_task_sync(self, task_description: str) -> dict:
        prompt = (
            """
            You are an expert software project estimator. Given a task description, estimate the effort required to complete the task. 
            Respond ONLY with a valid JSON object in the following format (no explanation, no markdown):
            {"unit": "hours", "value": <float>}
            Task: {task_description}
            """
        )
        prompt = prompt.replace("{task_description}", task_description)
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = httpx.post(f"{self.base_url}/api/generate", json=payload, timeout=30)
            response.raise_for_status()
            raw_output = response.json().get("response", "")
            # Try to extract JSON from the output
            json_start = raw_output.find('{')
            json_end = raw_output.rfind('}')
            if json_start != -1:
                # If closing brace is missing, fix it
                if json_end == -1:
                    json_str = raw_output[json_start:] + '}'
                else:
                    json_str = raw_output[json_start:json_end+1]
            else:
                json_str = raw_output.strip()
            try:
                return json.loads(json_str)
            except Exception as e:
                if custom_logger:
                    try:
                        custom_logger.error(f"LLM response not valid JSON: {raw_output}")
                    except Exception:
                        logging.error(f"LLM response not valid JSON: {raw_output}")
                else:
                    logging.error(f"LLM response not valid JSON: {raw_output}")
                # Fallback: try to fix missing closing brace
                if json_str and not json_str.strip().endswith('}'): 
                    json_str_fixed = json_str.strip() + '}'
                    try:
                        return json.loads(json_str_fixed)
                    except Exception:
                        pass
                # Log the error with standard logging if custom logger fails
                if custom_logger:
                    try:
                        custom_logger.error(f"LLM JSON parse error: {e}")
                    except Exception:
                        logging.error(f"LLM JSON parse error: {e}")
                else:
                    logging.error(f"LLM JSON parse error: {e}")
                return {"unit": "hours", "value": 8.0, "error": "llm_parse_failed"}
        except Exception as e:
            if custom_logger:
                try:
                    custom_logger.error(f"OllamaProvider error: {e}")
                except Exception:
                    logging.error(f"OllamaProvider error: {e}")
            else:
                logging.error(f"OllamaProvider error: {e}")
            return {"unit": "hours", "value": 8.0, "error": "llm_request_failed"}

    async def analyze_plan(self, plan_summary: dict, constraints: dict) -> str:
        # Stub implementation for compatibility
        return "Ollama analyze_plan not implemented."

    def _format_messages(self, messages: List[Dict[str, str]], json_mode: bool) -> str:
        """Format messages for Ollama."""
        if json_mode:
            messages.append({"role": "system", "content": "Provide your response as a valid JSON object."})
        formatted = []
        for msg in messages:
            if msg["role"] == "system":
                formatted.append(f"[INST] <<SYS>>{msg['content']}<</SYS>>")
            else:
                formatted.append(f"[INST] {msg['content']} [/INST]")
        return "\n".join(formatted)
