# FraudGraph — Architecture Conventions

## 1. Project Overview

FraudGraph is a graph-based fraud detection and investigation system. It combines transaction processing, graph relationships, rule-based signals, machine-learning risk scoring, and analyst review.

The backend is built with FastAPI and Python. PostgreSQL stores structured application data, Neo4j stores entity relationships, and Redis supports caching and short-lived application data.

## 2. Technology Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| Data validation | Pydantic v2 |
| Configuration | pydantic-settings |
| Relational database | PostgreSQL 17 |
| Graph database | Neo4j Community 5 |
| Cache | Redis 7 |
| ORM | SQLAlchemy 2 |
| Frontend | React + TypeScript + Vite |
| Testing | pytest, Vitest |
| Code quality | Ruff, Black, mypy |

## 3. Backend Module Boundaries

- `app/api/`: HTTP routes and API versioning.
- `app/core/`: configuration, logging, and shared application infrastructure.
- `app/db/`: PostgreSQL connections, ORM models, and persistence.
- `app/graph/`: Neo4j connectivity and graph operations.
- `app/schemas/`: Pydantic request and response contracts.
- `app/services/`: application-level business workflows.
- `app/features/`: feature extraction and feature engineering.
- `app/rules/`: deterministic fraud detection rules.
- `app/ml/`: model loading, inference, and evaluation utilities.
- `app/workers/`: asynchronous and background processing.

Keep HTTP handling, business logic, persistence, graph operations, and model inference separated.

## 4. Data and API Conventions

- Validate external input at API boundaries using Pydantic schemas.
- Reject unknown fields unless a schema explicitly allows them.
- Use timezone-aware timestamps and normalize transaction timestamps to UTC.
- Represent currency using three-letter uppercase currency codes.
- Use stable identifiers for transactions and related entities.
- Keep optional entity relationships nullable when the source transaction does not provide them.
- Keep the final risk score separate from optional model probability.
- Do not present model probability as available when no model inference has occurred.
- Keep analyst decisions separate from ground-truth fraud labels.

## 5. Initial API Contracts

The initial schemas are defined in `app/schemas/`:

- `NormalizedTransaction`: canonical transaction input.
- `TransactionResponse`: transaction ingestion outcome.
- `RiskScoreResponse`: risk score, risk level, rule signals, and optional model evidence.
- `AlertResponse`: alert details and lifecycle status.
- `AnalystDecisionRequest`: analyst decision, analyst identifier, and optional rationale.

These are initial API contracts. Their fields may evolve through explicit, tested schema changes.

## 6. Storage Responsibilities

### PostgreSQL

Use PostgreSQL for structured application records, including transaction metadata, alerts, analyst decisions, and other relational data.

### Neo4j

Use Neo4j for relationships between entities such as accounts, users, devices, IP addresses, cards, and merchants.

### Redis

Use Redis for caching and short-lived data. Cached values must have explicit expiration policies where appropriate.

## 7. Security and Configuration

- Read environment-specific settings from environment variables or `.env`.
- Never commit `.env` or real credentials.
- Keep `.env.example` updated with required configuration keys and safe placeholder values.
- Do not hardcode credentials in application code.
- Avoid logging secrets, passwords, or sensitive transaction data.

## 8. Testing and Quality

- Put unit tests under `backend/tests/unit/`.
- Put integration tests under `backend/tests/integration/`.
- Test schema validation, boundary conditions, and invalid inputs.
- Run automated tests before committing.
- Use Ruff and Black for code quality and formatting.
- Use mypy for static type checking.

## 9. Development Principles

1. Prefer explicit contracts over implicit assumptions.
2. Keep modules small and responsibilities focused.
3. Make local setup reproducible.
4. Keep deterministic rules distinguishable from ML outputs.
5. Make important decisions observable and testable.
6. Document architectural changes when they affect module boundaries or API contracts.
