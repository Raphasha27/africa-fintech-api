# Africa Fintech API

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A production-ready mobile money / fintech REST API inspired by systems like M-Pesa. Built with FastAPI, SQLAlchemy (Async), and JWT authentication.

## Features
- **User Authentication:** Secure JWT-based auth (register, login).
- **Wallet Management:** Auto-provisioned digital wallets with multi-currency support.
- **Transactions:** Atomic P2P money transfers ensuring data integrity.
- **FX & Remittance:** Exchange rates simulation for cross-border African transfers (ZAR, KES, NGN, GHS, USD).

## Quick Start (Docker)
`ash
docker-compose up --build
`
API Documentation (Swagger UI) available at: http://localhost:8000/docs

## Core Stack
- Python 3.11
- FastAPI + Pydantic v2
- SQLAlchemy 2.0 (Async)
- SQLite (Local) / PostgreSQL (Prod ready)
