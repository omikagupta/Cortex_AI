# AI Workspace Agent

AI Workspace Agent is a production-grade AI-powered knowledge workspace built with FastAPI, PostgreSQL, Redis, LangChain, Ollama, and modern backend engineering practices.

It is designed as an enterprise SaaS application rather than a simple "Chat with PDF" project.

---

## Features

### Backend Engineering

- Clean Architecture
- Repository Pattern
- Service Layer
- Dependency Injection
- Centralized Configuration
- Standardized API Responses
- Global Exception Handling
- Centralized Logging

### AI Engineering (Upcoming)

- RAG Pipeline
- Hybrid Search
- Multi-Agent Architecture
- Workspace Memory
- Semantic Search
- Citation Engine
- Flashcard Generator
- Resume Intelligence

### DevOps

- Docker
- Docker Compose
- GitHub Actions
- NGINX
- Production Deployment

---

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Redis
- Celery

### AI

- LangChain
- Ollama
- Gemma 3
- Sentence Transformers
- ChromaDB

### Frontend

- Next.js
- React
- TailwindCSS
- TypeScript

---

## Project Structure

```text
app/
├── api/
├── ai/
├── core/
├── db/
├── models/
├── repositories/
├── schemas/
├── services/
├── utils/
├── workers/
└── tests/
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=ai_workspace
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

SECRET_KEY=change_this

REDIS_HOST=localhost
REDIS_PORT=6379

OLLAMA_BASE_URL=http://localhost:11434
```

Run the application

```bash
python -m uvicorn app.main:app --reload
```

---

## API Documentation

Swagger

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## Current Endpoints

| Method | Endpoint |
|---------|----------|
| GET | /api/v1/health |

---

## Roadmap

- Production Backend
- Authentication
- Workspace Engine
- RAG Engine
- Resume Intelligence
- AI Learning Engine
- Agentic AI
- Workspace Intelligence
- DevOps
- Production Deployment

---

## License

MIT