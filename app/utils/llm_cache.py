import hashlib
import json
from typing import Dict, Any

class LLMCache:
    """Simple in-memory cache for LLM estimation results."""
    def __init__(self):
        self._cache = {}

    def _make_key(self, prompt: str, params: Dict[str, Any]) -> str:
        key_data = json.dumps({"prompt": prompt, "params": params}, sort_keys=True)
        return hashlib.sha256(key_data.encode()).hexdigest()

    def get(self, prompt: str, params: Dict[str, Any]) -> Any:
        key = self._make_key(prompt, params)
        return self._cache.get(key)

    def set(self, prompt: str, params: Dict[str, Any], result: Any) -> None:
        key = self._make_key(prompt, params)
        self._cache[key] = result

llm_cache = LLMCache()
