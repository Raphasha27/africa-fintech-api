<div align="center">

# Africa Fintech API

**Production-Grade Mobile Money API for Africa — Inspired by M-Pesa**

[![CI](https://github.com/Raphasha27/africa-fintech-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphasha27/africa-fintech-api/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Quality](https://img.shields.io/badge/code%20quality-ruff-4B2E83)](https://docs.astral.sh/ruff/)
[![Test Coverage](https://img.shields.io/badge/test%20coverage-90%25-brightgreen)](https://github.com/Raphasha27/africa-fintech-api)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker)](https://github.com/Raphasha27/africa-fintech-api)

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)

</div>

---

## Features

- **User Registration & JWT Auth** — Secure account creation with stateless token authentication
- **Multi-Currency Wallets** — ZAR, KES, NGN, GHS, USD balance support
- **Peer-to-Peer Transfers** — Instant cross-wallet money transfers with idempotency
- **Deposit & Funding** — Wallet top-up simulation for testing flows
- **Transaction History** — Complete audit trail for all wallet operations
- **Rate Limiting** — Redis-backed API rate limiting for abuse prevention
- **Cross-Border Remittance** — Multi-currency conversion simulation

---

## Quick Start

```bash
git clone https://github.com/Raphasha27/africa-fintech-api.git
cd africa-fintech-api
docker-compose up --build
```

API docs (Swagger UI): `http://localhost:8000/docs`

---

## Architecture

> Full architecture documentation: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   Client     │──────▶│   FastAPI     │──────▶│  PostgreSQL   │
│  (Mobile/    │  HTTP │   (Python    │  SQL  │  (Async via   │
│   Web)       │◀──────│   3.12)      │◀──────│   SQLAlchemy) │
└──────────────┘       └──────┬───────┘       └──────────────┘
                              │
                     ┌────────▼────────┐
                     │     Redis       │
                     │  (Cache/Queue)  │
                     └─────────────────┘
```

---

## API Documentation

> Full API reference: [docs/API.md](docs/API.md) · Swagger UI: `http://localhost:8000/docs`

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Register a new user | None |
| POST | `/api/v1/auth/login` | Login and receive JWT | None |
| GET | `/api/v1/auth/me` | Get current user profile | Bearer |

### Wallets

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/wallets` | Create a new wallet | Bearer |
| GET | `/api/v1/wallets/me` | Get wallet balance | Bearer |
| POST | `/api/v1/wallets/fund` | Fund wallet (deposit) | Bearer |

### Transactions

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/transactions/transfer` | P2P money transfer | Bearer |
| GET | `/api/v1/transactions/history` | Transaction history | Bearer |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |

---

## Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| Language | Python 3.12 | Modern async runtime |
| Framework | FastAPI | High-performance async web framework |
| ORM | SQLAlchemy 2.0 | Async ORM with PostgreSQL/SQLite support |
| Validation | Pydantic v2 | Data validation and settings management |
| Auth | python-jose (JWT) | Stateless token authentication |
| Cache | Redis | Caching and rate limiting |
| Container | Docker + Compose | Containerized deployment |

---

## Project Structure

```
africa-fintech-api/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI application factory
│   ├── config.py           # Pydantic Settings
│   ├── models.py           # SQLAlchemy ORM models
│   ├── dependencies.py     # DB sessions & JWT auth
│   └── routers/
│       ├── __init__.py
│       ├── auth.py         # Registration & login
│       ├── wallets.py      # Wallet CRUD & funding
│       └── transactions.py # P2P transfers & history
├── tests/
│   ├── conftest.py         # Shared fixtures
│   ├── test_auth.py
│   ├── test_wallets.py
│   └── test_transactions.py
├── docs/
│   ├── ARCHITECTURE.md     # System architecture
│   └── API.md              # API reference
├── .github/workflows/
│   └── ci.yml              # GitHub Actions CI
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
└── README.md
```

---

## Testing

```bash
pip install -e ".[dev]"
pytest --cov=app --cov-report=term-missing
```

---

## Deployment

### Docker

```bash
docker-compose up --build -d
docker-compose logs -f      # View live logs
docker-compose down          # Stop all services
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./test.db` | Database connection string |
| `REDIS_URL` | `redis://redis:6379` | Redis connection string |
| `JWT_SECRET_KEY` | — | Secret key for JWT signing |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | JWT token expiry |

### Local Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and open an issue before submitting a PR.

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Built by <a href="https://github.com/Raphasha27">Koketso Raphasha</a> · <a href="https://portfolio-iota-eight-90.vercel.app/">Portfolio</a>
</div>
