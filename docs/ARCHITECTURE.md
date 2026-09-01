# Africa Fintech API — Architecture

## System Overview

Africa Fintech API is a production-ready mobile money and fintech REST API inspired by systems like M-Pesa. It supports user wallets, peer-to-peer transfers, multi-currency balances (ZAR, KES, NGN, GHS, USD), and cross-border remittance simulation. Built with FastAPI and async SQLAlchemy for high-concurrency financial operations.

## Architecture Diagram

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│   Client     │──────►│   FastAPI        │──────►│  PostgreSQL   │
│  (Mobile/    │  HTTP │   (Python 3.12)  │  SQL  │  (Async via   │
│   Web)       │◄──────│   Uvicorn ASGI   │◄──────│  SQLAlchemy)  │
└──────────────┘       └───────┬──────────┘       └──────────────┘
                               │
                      ┌────────▼────────┐
                      │     Redis       │
                      │  (Cache/Queue)  │
                      └─────────────────┘
```

## Technology Stack

| Component      | Technology                    | Version  |
|----------------|-------------------------------|----------|
| Language       | Python                        | 3.12     |
| Framework      | FastAPI                       | 0.115.0  |
| ASGI Server    | Uvicorn                       | 0.52.4   |
| ORM            | SQLAlchemy (async)            | 2.0.36   |
| DB Driver      | aiosqlite                     | 0.20.0   |
| Validation     | Pydantic (pydantic-settings)  | 2.15.0   |
| Auth           | python-jose (JWT)             | 3.3.0    |
| Password Hash  | passlib (bcrypt)              | 1.7.4    |
| Form Parsing   | python-multipart              | 0.0.12   |
| Container      | Docker, docker-compose        | —        |
| CI/CD          | GitHub Actions                | —        |

## Directory Structure

```
africa-fintech-api/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application factory
│   ├── config.py              # Pydantic Settings (env-based config)
│   ├── models.py              # SQLAlchemy ORM models (User, Wallet, Transaction)
│   ├── dependencies.py        # DB session injection & JWT auth dependency
│   └── routers/
│       ├── __init__.py
│       ├── auth.py            # POST /register, /login, GET /me
│       ├── wallets.py         # POST /wallets, /fund; GET /wallets/me
│       └── transactions.py    # POST /transfer; GET /history
├── tests/
│   ├── conftest.py            # Shared fixtures (test DB, auth tokens)
│   ├── test_auth.py
│   ├── test_wallets.py
│   └── test_transactions.py
├── .github/workflows/ci.yml   # GitHub Actions CI pipeline
├── pyproject.toml             # Project metadata + ruff config
├── requirements.txt           # Runtime dependencies
├── Dockerfile                 # Multi-stage Python build
├── docker-compose.yml         # App + PostgreSQL + Redis
└── README.md
```

## Data Flow

### Registration & Authentication
1. Client sends `POST /api/v1/auth/register` with email + password.
2. Password is hashed with bcrypt via passlib.
3. User record created in PostgreSQL.
4. Client sends `POST /api/v1/auth/login` → returns JWT access token.
5. Subsequent requests include `Authorization: Bearer <token>` header.
6. `get_current_user()` dependency decodes JWT and injects user context.

### Wallet Operations
1. `POST /api/v1/wallets` — Creates a wallet for authenticated user with specified currency.
2. `POST /api/v1/wallets/fund` — Deposits funds, updates balance atomically.
3. `GET /api/v1/wallets/me` — Returns wallet balance and currency.

### P2P Transfer
1. Client sends `POST /api/v1/transactions/transfer` with recipient ID and amount.
2. System validates sufficient balance, creates debit/credit records in single transaction.
3. Atomic commit ensures balance consistency — no partial transfers.

## Security

- **JWT Authentication**: Stateless token-based auth with configurable expiry via `SECRET_KEY` environment variable.
- **Password Hashing**: bcrypt with passlib — industry-standard slow hash resistant to brute-force.
- **SQL Injection Prevention**: SQLAlchemy ORM parameterizes all queries; no raw SQL.
- **CORS**: Configured per environment; restrict origins in production.
- **Input Validation**: Pydantic v2 validates all request/response schemas at the framework level.
- **Environment Variables**: Secrets (`SECRET_KEY`, `DATABASE_URL`) loaded from env, never committed.

## Deployment

### Docker (Recommended)

```bash
docker-compose up --build
```

API docs (Swagger UI): `http://localhost:8000/docs`

### Local Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

### Environment Variables

| Variable       | Default                        | Description          |
|----------------|--------------------------------|----------------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./db.db`  | SQLAlchemy DB URL    |
| `SECRET_KEY`   | (required)                     | JWT signing key      |
| `REDIS_URL`    | `redis://localhost:6379`        | Cache backend        |

## Scaling Considerations

- **Database**: Migrate from SQLite to PostgreSQL/MySQL for production; use connection pooling via SQLAlchemy pool settings.
- **Horizontal scaling**: Deploy multiple Uvicorn workers (`--workers N`) behind a load balancer; use Redis for shared session state.
- **Rate limiting**: Implement Redis-based rate limiting per user/IP to prevent abuse.
- **Async I/O**: Full async stack (FastAPI + aiosqlite/asyncpg) handles high concurrency without thread blocking.
- **Caching**: Cache wallet balances and transaction history in Redis to reduce DB reads.
- **Queue integration**: Offload heavy operations (remittance, notifications) to Celery/RQ with Redis broker.

## Decision Records

| Decision | Rationale |
|----------|-----------|
| FastAPI over Flask | Native async support, automatic OpenAPI docs, Pydantic validation built-in |
| SQLAlchemy 2.0 async | Modern async ORM with mature ecosystem; supports both SQLite (dev) and PostgreSQL (prod) |
| JWT over sessions | Stateless auth scales horizontally without shared session store |
| Pydantic v2 | 5-50x faster validation than v1; native type coercion for financial amounts |
| Single-service architecture | Simpler deployment for MVP; split to microservices when team/process requires it |
| Redis for cache | Industry-standard in-memory store; trivial to swap to Memcached |
