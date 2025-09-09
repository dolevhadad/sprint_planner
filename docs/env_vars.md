# Environment Variables

| Variable              | Description                                 | Example Value                |
|-----------------------|---------------------------------------------|------------------------------|
| MODEL_PROVIDER        | LLM provider: ollama or bedrock             | ollama                       |
| OLLAMA_BASE_URL       | Ollama API base URL                         | http://localhost:11434       |
| OLLAMA_MODEL          | Ollama model name                           | llama2                       |
| AWS_REGION            | AWS region for Bedrock                      | us-east-1                    |
| AWS_ACCESS_KEY_ID     | AWS credentials (Bedrock)                   | your_key                     |
| AWS_SECRET_ACCESS_KEY | AWS credentials (Bedrock)                   | your_secret                  |
| BEDROCK_MODEL         | Bedrock model name                          | anthropic.claude-v2          |
| API_HOST              | API host                                    | 0.0.0.0                      |
| API_PORT              | API port                                    | 8000                         |
| LOG_LEVEL             | Logging level                               | INFO                         |

## Usage
- Copy `.env.example` to `.env` and edit as needed.
- All variables can be overridden in Docker Compose or CI/CD.
