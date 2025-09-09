# Quickstart Guide

## 1. Clone and Install
```bash
git clone https://github.com/dolevhadad/sprint_planning.git
cd sprint_planning
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 2. Configure Environment
```bash
cp .env.example .env
```
Edit `.env` for Ollama or Bedrock settings.

## 3. Run Locally
```bash
uvicorn app.api.routes:app --reload --host 0.0.0.0 --port 8000
```

## 4. Use Docker
```bash
docker-compose up --build
```

## 5. Test API
- Health: `GET /health`
- Plan: `POST /plan/sprint` (see `data/samples/sample_plan_request.json`)
- Change LLM model: `POST /llm/model` with `{ "provider": "ollama", "model": "llama2" }`

## 6. Run Tests
```bash
pytest tests/
```

## 7. Explore Docs
- See `docs/architecture.md` for diagrams
- See `README.md` for full usage
