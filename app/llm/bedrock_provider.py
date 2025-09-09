import boto3
import json
from typing import Dict, Any, Optional, List
from app.llm.base import LLMClient
from app.core.config import get_settings

settings = get_settings()

class BedrockProvider(LLMClient):
    def __init__(self):
        self.session = boto3.Session(region_name=settings.AWS_REGION)
        self.client = self.session.client('bedrock-runtime')
        self.model = settings.BEDROCK_MODEL

    async def chat(self, 
                  messages: List[Dict[str, str]], 
                  json_mode: bool = False,
                  tools: Optional[List[Dict[str, Any]]] = None) -> str:
        """Send a chat request to AWS Bedrock."""
        
        # Format messages for the specific model (example for Claude)
        formatted_messages = self._format_messages(messages, json_mode)
        
        response = await self._invoke_model(formatted_messages)
        return self._parse_response(response)

    async def estimate_task(self, task_description: str, required_skills: List[str]) -> Dict[str, Any]:
        """Estimate effort for a task."""
        
        messages = [
            {"role": "system", "content": "You are an expert project estimator. Analyze the task and required skills to provide an effort estimate in hours."},
            {"role": "user", "content": f"Task: {task_description}\nRequired skills: {', '.join(required_skills)}"}
        ]
        
        response = await self.chat(messages, json_mode=True)
        return json.loads(response)

    async def analyze_plan(self, plan_summary: Dict[str, Any], constraints: Dict[str, Any]) -> str:
        """Analyze a sprint plan."""
        
        messages = [
            {"role": "system", "content": "You are a sprint planning expert. Analyze the plan and provide insights."},
            {"role": "user", "content": f"Plan summary: {json.dumps(plan_summary)}\nConstraints: {json.dumps(constraints)}"}
        ]
        
        return await self.chat(messages)

    def _format_messages(self, messages: List[Dict[str, str]], json_mode: bool) -> Dict[str, Any]:
        """Format messages for Bedrock models."""
        if self.model.startswith('anthropic.claude'):
            return self._format_for_claude(messages, json_mode)
        # Add support for other models as needed
        raise ValueError(f"Unsupported model: {self.model}")

    def _format_for_claude(self, messages: List[Dict[str, str]], json_mode: bool) -> Dict[str, Any]:
        """Format messages for Claude models."""
        if json_mode:
            messages.append({"role": "system", "content": "Provide your response as a valid JSON object."})

        prompt = "\n\n".join([
            f"{'Assistant' if msg['role'] == 'assistant' else 'Human'}: {msg['content']}"
            for msg in messages
        ])

        return {
            "prompt": prompt + "\n\nAssistant:",
            "max_tokens": 2048,
            "temperature": 0.1 if json_mode else 0.7,
            "top_p": 1,
            "stop_sequences": ["\n\nHuman:"]
        }

    async def _invoke_model(self, request_body: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke the Bedrock model."""
        response = self.client.invoke_model(
            body=json.dumps(request_body),
            modelId=self.model,
            contentType='application/json',
            accept='application/json'
        )
        return json.loads(response['body'].read())

    def _parse_response(self, response: Dict[str, Any]) -> str:
        """Parse the response from Bedrock."""
        if self.model.startswith('anthropic.claude'):
            return response.get('completion', '')
        # Add support for other models as needed
        raise ValueError(f"Unsupported model: {self.model}")
