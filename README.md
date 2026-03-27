# TT-Migrate: Tenstorrent Model Migration Sandbox

A web-based developer tool that analyzes PyTorch scripts and visually maps incompatible operations to native Tenstorrent ttnn APIs before hardware compilation.

## Overview

TT-Migrate reduces "Time-to-First-Successful-Compile" by surfacing exactly what needs to change when porting PyTorch models to Tenstorrent hardware, then offers AI-powered one-click refactoring.

### Core Features

- **AST Code Parser** - Parses Python source code and identifies PyTorch API calls incompatible with TT-Forge/ttnn
- **Split-Screen Editor** - Monaco-based editor showing original code alongside ttnn-optimized suggestions
- **Constraint Explainer** - Human-readable tooltips explaining hardware constraints for each flagged operation
- **LLM-Powered Refactoring** - AI code transformation supporting Claude, GPT-4, and Gemini backends
- **Export** - Download refactored code as .py, .ipynb, or migration report

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optional)

### Using Docker Compose

```bash
cp .env.example .env
# Edit .env with your LLM API keys

docker-compose up
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

**Backend:**

```bash
cd server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm start
```

### Running Tests

```bash
cd server
pytest tests/ -v
```

## Architecture

```
Frontend (React + Monaco Editor)
        │
        │ REST API + SSE
        ▼
Backend (FastAPI)
  ├── AST Parser Service
  ├── Compatibility Matrix (JSON)
  ├── LLM Router (Anthropic / OpenAI / Google)
  └── Export Service (.py / .ipynb / .md)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/analyze` | Parse PyTorch code and return diagnostics |
| POST | `/api/v1/refactor` | LLM-powered code refactoring |
| POST | `/api/v1/export` | Generate downloadable files |
| GET | `/api/v1/compatibility` | Query the compatibility matrix |
| GET | `/api/v1/health` | Health check |

## Configuration

Set environment variables or create a `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | Default LLM backend (anthropic/openai/google) | anthropic |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `GOOGLE_API_KEY` | Google AI API key | - |
| `CORS_ORIGINS` | Allowed CORS origins | http://localhost:3000 |

## License

MIT
