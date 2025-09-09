from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

class LLMClient(ABC):
    """Base class for LLM providers."""
    
    @abstractmethod
    async def chat(self, 
                  messages: list[Dict[str, str]], 
                  json_mode: bool = False,
                  tools: Optional[list[Dict[str, Any]]] = None) -> str:
        """
        Send a chat request to the LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            json_mode: Whether to request JSON output
            tools: Optional list of tool specifications
            
        Returns:
            The LLM response as a string
        """
        pass

    @abstractmethod
    async def estimate_task(self, task_description: str, required_skills: list[str]) -> Dict[str, Any]:
        """
        Estimate effort for a task based on description and required skills.
        
        Args:
            task_description: The task description
            required_skills: List of required skill names
            
        Returns:
            Dictionary with estimation details
        """
        pass

    @abstractmethod
    async def analyze_plan(self, 
                         plan_summary: Dict[str, Any],
                         constraints: Dict[str, Any]) -> str:
        """
        Analyze a sprint plan and provide insights.
        
        Args:
            plan_summary: The plan summary details
            constraints: The planning constraints used
            
        Returns:
            Analysis and recommendations as a string
        """
        pass
