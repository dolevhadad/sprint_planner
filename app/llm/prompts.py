"""Collection of prompts for LLM interactions."""

TASK_ESTIMATION_PROMPT = """You are an expert project estimator.
Analyze the task description and required skills to provide an effort estimate in hours.

Task: {task_description}
Required skills: {skills}

Respond with a JSON object in this format:
{
    "unit": "hours",
    "value": <number>,
    "confidence": "high|medium|low",
    "reasoning": "<brief explanation>"
}

Base your estimate on:
1. Task complexity and scope
2. Required skills and their interdependencies
3. Similar tasks in typical development environments

Provide realistic estimates suitable for sprint planning."""

PLAN_ANALYSIS_PROMPT = """You are a sprint planning expert.
Review the sprint plan details and provide insights on its feasibility and risks.

Plan Summary:
{plan_summary}

Planning Constraints:
{constraints}

Focus your analysis on:
1. Team utilization and workload balance
2. Skill coverage and potential bottlenecks
3. Dependencies and critical path
4. Risks and mitigation suggestions

Provide a concise, actionable analysis that helps the team make decisions."""

SKILL_MATCHING_PROMPT = """You are a technical skills expert.
Analyze the required skills for a task and compare them to available team members.

Required Skills:
{required_skills}

Available Team Members and Skills:
{team_skills}

Respond with a JSON object listing suitable team members and explaining the match:
{
    "matches": [
        {
            "employee_id": "<id>",
            "match_score": <0-100>,
            "reasoning": "<brief explanation>"
        }
    ],
    "suggestions": ["<any recommendations for skill development or team composition>"]
}"""
