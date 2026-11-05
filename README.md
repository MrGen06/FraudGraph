# FraudGraph

**Graph-Based Fraud Detection and Investigation Platform**

FraudGraph is a fraud detection and investigation platform designed to identify suspicious financial transactions using graph-based relationship analysis, rule-based detection, and machine learning.

## Technology Stack

| Layer | Technologies |
|---|---|
| Backend | Python 3.12, FastAPI, Pydantic v2 |
| Database | PostgreSQL 17 |
| Graph Database | Neo4j 5 Community |
| Cache | Redis 7 |
| Frontend | React 19, TypeScript, Vite |
| Graph Visualization | Cytoscape.js |
| Testing | Pytest, Vitest, React Testing Library |
| Code Quality | Ruff, Black, MyPy, ESLint, Pre-commit |
| Infrastructure | Docker Compose |

## Project Structure

```text
FraudGraph/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── features/
│   │   ├── graph/
│   │   ├── ml/
│   │   ├── rules/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── workers/
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   └── .venv/
├── frontend/
│   ├── src/
│   └── package.json
├── docker/
│   └── docker-compose.yml
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   └── architecture.md
├── models/
├── notebooks/
├── scripts/
├── .env.example
└── README.md
```

## Prerequisites

- Python 3.12
- Node.js and npm
- Docker Desktop with Docker Compose
- Git

## Local Development Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd FraudGraph
```

### 2. Configure environment variables

Create your local environment file from the example:

```powershell
Copy-Item .env.example .env
```

Update `.env` with your local credentials and configuration.

**Never commit `.env` or expose credentials in source control.**

### 3. Start infrastructure services

```powershell
docker compose --env-file .env -f docker/docker-compose.yml up -d
```

Services:

| Service | Local Port |
|---|---:|
| PostgreSQL | 5432 |
| Neo4j HTTP | 7474 |
| Neo4j Bolt | 7687 |
| Redis | 6379 |

### 4. Set up the backend

```powershell
py -3.12 -m venv backend/.venv
.\backend\.venv\Scripts\Activate.ps1
```

Install the backend dependencies using the project's dependency manifest once established.

Start the API from the `backend` directory:

```powershell
python -m uvicorn app.main:app --reload
```

API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Health endpoints:

- Liveness: http://localhost:8000/health/live
- Readiness: http://localhost:8000/health/ready

### 5. Set up the frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend development server: http://localhost:5173

## Validation Commands

### Backend

Run from `backend/` with its virtual environment activated:

```powershell
python -m pytest -q
python -m ruff check app tests
python -m ruff format --check app tests
python -m mypy app tests
pre-commit run --all-files
```

### Frontend

Run from `frontend/`:

```powershell
npm run build
npm run lint
npm test
```

## Documentation

- [Architecture Documentation](docs/architecture.md)

## Development Status

The initial development foundation includes:

- Repository and modular project structure.
- Environment-based application configuration.
- Docker-based PostgreSQL, Neo4j, and Redis services.
- FastAPI application and health endpoints.
- Canonical Pydantic schemas.
- Backend unit tests and static code-quality checks.
- React and TypeScript frontend scaffold.
- Frontend build, lint, and test infrastructure.

Further development will follow the project's 10-day execution plan.

## Security Notes

- Keep secrets in `.env`.
- Do not commit credentials, API keys, or private datasets.
- Validate incoming transaction data before processing.
- Use stable identifiers for transaction entities and relationships.
