# Sprint Planning Assistant

An intelligent sprint planning system that uses LLM (Language Learning Models) to optimize task assignments and sprint planning. The system takes into account team member skills, availability, and task requirements to create optimal sprint plans.

## Features

- 🤖 LLM-powered task estimation
- 📊 Intelligent task assignment optimization
- 👥 Team skill matching and utilization
- 📅 Sprint capacity planning
- 🔄 Support for both Ollama (local) and AWS Bedrock

## Architecture

```
app/
├── api/          # FastAPI endpoints
├── core/         # Core configuration and logging
├── domain/       # Domain models and enums
├── llm/          # LLM integration (Ollama/Bedrock)
├── schemas/      # API request/response schemas
├── services/     # Business logic
└── utils/        # Helper utilities
```

## Prerequisites

- Python 3.9+
- Ollama (for local LLM) or AWS account (for Bedrock)
- PuLP for optimization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dolevhadad/sprint_planning.git
cd sprint_planning
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
MODEL_PROVIDER=ollama  # or bedrock
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# If using AWS Bedrock:
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
BEDROCK_MODEL=anthropic.claude-v2
```

## Running the Service

Start the API server:
```bash
uvicorn app.api.routes:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

## API Usage

### Plan a Sprint

POST `/plan/sprint`

Request body example:
```json
{
  "sprint": {
    "id": "SPR-2025-09",
    "name": "September Sprint",
    "start_date": "2025-09-15",
    "end_date": "2025-09-29",
    "timezone": "UTC",
    "work_days": 10,
    "work_hours_per_day": 8
  },
  "teams": [...],
  "employees": [...],
  "tasks": [...],
  "constraints": {
    "max_parallel_tasks_per_person": 2,
    "allow_cross_team": false
  }
}
```

See `data/samples/sample_plan_request.json` for a complete example.

### Health Check

GET `/health`

## Key Components

### Task Estimation

- Uses LLM to estimate task effort when not provided
- Considers task description and required skills
- Falls back to configurable defaults if needed

### Skill Matching

- Supports both threshold and weighted matching policies
- Normalizes skill names (e.g., "js" → "javascript")
- Considers skill levels (1-5 scale)

### Assignment Optimization

Uses PuLP to optimize assignments considering:
- Employee capacity and skills
- Task priorities and dependencies
- Team WIP limits
- Cross-team restrictions

### Plan Validation

Validates:
- Sprint dates and holidays
- Team structure
- Employee skills and capacity
- Task dependencies (including cycle detection)

## Configuration Options

### LLM Providers

#### Ollama (Local)
- Free, runs locally
- Supports various models
- Good for development and testing

#### AWS Bedrock
- Production-grade
- Supports multiple models (Claude, Llama2)
- Better reliability and performance

### Planning Constraints

- `max_parallel_tasks_per_person`: Limit concurrent tasks
- `allow_cross_team`: Enable/disable cross-team assignments
- `match_policy`: "threshold" or "weighted" skill matching
- `min_skill_level_match`: Allowed skill level gap (0-2)

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black .
isort .
flake8
```

## Troubleshooting

1. LLM Connection Issues
   - For Ollama: Ensure the service is running (`ollama serve`)
   - For Bedrock: Verify AWS credentials and permissions

2. Optimization Failures
   - Check task dependencies for cycles
   - Verify skill requirements match available team skills
   - Ensure sufficient capacity in the sprint

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
