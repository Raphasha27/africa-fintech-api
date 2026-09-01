# Contributing to Africa Fintech API

Welcome and thank you for your interest in contributing to **Africa Fintech API**! Every contribution helps make mobile money infrastructure better for Africa.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Architecture Reference](#architecture-reference)
- [Release Process](#release-process)

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code. Please report unacceptable behavior to **raphasha27@github.com**.

---

## Development Setup

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12+ | Runtime |
| Docker | 24.x+ | Containerized development |
| Docker Compose | v2.x+ | Multi-service orchestration |
| pip | Latest | Dependency management |

### Step-by-Step Setup

1. **Fork and clone** the repository:
   ```bash
   git clone https://github.com/<your-username>/africa-fintech-api.git
   cd africa-fintech-api
   ```

2. **Start the development environment**:
   ```bash
   docker-compose up --build
   ```

3. **Verify services are running**:
   - API (Swagger UI): `http://localhost:8000/docs`
   - PostgreSQL: `localhost:5432`
   - Redis: `localhost:6379`

4. **Run linter locally** (optional):
   ```bash
   ruff check .
   ruff format .
   ```

5. **Run tests locally**:
   ```bash
   pytest tests/ -v --cov=src --cov-report=term-missing
   ```

---

## Code Style Guidelines

### Python (FastAPI)

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide.
- Use **Ruff** for linting and formatting — CI enforces this.
- Maximum line length: **88 characters** (Ruff default).
- Use type hints on all function signatures.
- Prefer async/await for I/O-bound operations (database, Redis).

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Functions | `snake_case` | `create_wallet` |
| Classes | `PascalCase` | `WalletService` |
| Constants | `UPPER_SNAKE_CASE` | `SUPPORTED_CURRENCIES` |
| API routes | `kebab-case` | `/api/v1/transfers` |
| Database columns | `snake_case` | `created_at` |

### General

- Write meaningful variable and function names.
- Add docstrings for all public functions and classes.
- Keep functions focused and under 40 lines.
- No hardcoded secrets — use environment variables.
- Prefer f-strings over `.format()` or `%` formatting.

---

## Testing Requirements

| Type | Framework | Coverage Target |
|------|-----------|-----------------|
| Unit tests | pytest | 85%+ |
| Integration tests | pytest + httpx | 80%+ |
| API tests | FastAPI TestClient | All endpoints |

- Every new feature **must** include tests.
- Bug fixes **must** include a regression test.
- Run the full test suite before pushing:
  ```bash
  pytest tests/ -v --cov=src --cov-report=term-missing
  ```
- Tests must pass with zero warnings.

---

## Pull Request Process

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines above.

3. **Write or update tests** to cover your changes.

4. **Commit with a conventional message**:
   ```
   feat: add cross-border remittance endpoint
   fix: correct idempotency key validation
   docs: update API documentation for wallet transfers
   test: add integration tests for P2P transfers
   chore: update FastAPI dependencies
   ```

5. **Push and open a PR** against `main`.

6. **PR checklist** (all must pass before merge):
   - [ ] CI pipeline passes (linting, tests, Docker build)
   - [ ] Code reviewed by at least one maintainer
   - [ ] No merge conflicts with `main`
   - [ ] API documentation updated (if applicable)
   - [ ] Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)

---

## Issue Guidelines

### Bug Reports

- Check [existing issues](../../issues) first to avoid duplicates.
- Include a clear, descriptive title.
- Provide steps to reproduce, expected vs. actual behavior.
- Include environment details: Python version, OS, Docker version.
- Attach API request/response logs if relevant.

### Feature Requests

- Describe the feature and its motivation.
- Explain the use case for African mobile money users.
- Propose an implementation approach if possible.

### Labels

| Label | Description |
|-------|-------------|
| `bug` | Something is broken |
| `enhancement` | New feature or improvement |
| `good-first-issue` | Ideal for first-time contributors |
| `security` | Security-related concern |
| `help-wanted` | Community help appreciated |

---

## Architecture Reference

For detailed system design, data flow diagrams, and component interactions, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Key components to understand:
- **FastAPI Backend** — REST API with async SQLAlchemy ORM
- **PostgreSQL** — Primary database with async connection pooling
- **Redis** — Rate limiting, caching, and session management
- **JWT Authentication** — Stateless token-based auth with refresh tokens

---

## Release Process

1. All changes merge to `main` via PR with passing CI.
2. Semantic versioning is used: `MAJOR.MINOR.PATCH`.
3. Tags are created for each release: `git tag v1.x.x`.
4. Docker images are built and published automatically via CI.
5. Release notes are generated from conventional commit messages.

---

## Questions?

Open a [discussion](../../discussions) or reach out to **raphasha27@github.com**.

Thank you for contributing to Africa Fintech API!
