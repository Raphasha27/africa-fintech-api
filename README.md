[![CI](https://github.com/Raphasha27/africa-fintech-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphasha27/africa-fintech-api/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Africa Fintech API

Production-Grade Mobile Money API for Africa

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)

## Overview

A production-ready mobile money and fintech REST API inspired by systems like M-Pesa. Supports user wallets, peer-to-peer transfers, multi-currency balances (ZAR, KES, NGN, GHS, USD), and cross-border remittance simulation.

## Architecture

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

## Quick Start

### Docker (Recommended)

```bash
docker-compose up --build
```

API documentation (Swagger UI): http://localhost:8000/docs

### Local Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## API Endpoints

| Method | Endpoint                    | Description              | Auth     |
|--------|-----------------------------|--------------------------|----------|
| POST   | `/api/v1/auth/register`     | Register a new user      | None     |
| POST   | `/api/v1/auth/login`        | Login and receive JWT     | None     |
| GET    | `/api/v1/auth/me`           | Get current user profile  | Bearer   |
| POST   | `/api/v1/wallets`           | Create a new wallet       | Bearer   |
| GET    | `/api/v1/wallets/me`        | Get wallet balance        | Bearer   |
| POST   | `/api/v1/wallets/fund`      | Fund wallet (deposit)     | Bearer   |
| POST   | `/api/v1/transactions/transfer` | P2P money transfer   | Bearer   |
| GET    | `/api/v1/transactions/history`  | Transaction history  | Bearer   |
| GET    | `/health`                   | Health check              | None     |

## Tech Stack

- **Python 3.12** — modern async runtime
- **FastAPI** — high-performance async web framework
- **SQLAlchemy 2.0** — async ORM with PostgreSQL/SQLite support
- **Pydantic v2** — data validation and settings management
- **JWT (python-jose)** — stateless authentication
- **Redis** — caching and rate limiting
- **Docker** — containerized deployment

## Directory Structure

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
├── .github/workflows/
│   └── ci.yml              # GitHub Actions CI
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## License

MIT
