"""Africa Fintech API — Production-grade mobile money backend."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.models import Base
from app.routers import auth, transactions, wallets

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Create database tables on startup for development."""
    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Africa Fintech API",
    description=(
        "Production-grade mobile money and remittance backend for African fintech markets.\n\n"
        "## Features\n"
        "- **Authentication** — Register, login, and JWT-based session management\n"
        "- **Wallets** — Create, fund, and query mobile money wallets\n"
        "- **Transactions** — Peer-to-peer transfers with full audit trail\n\n"
        "## Authentication\n"
        "All protected endpoints require a JWT Bearer token. Obtain one via `/api/v1/auth/login` "
        "or `/api/v1/auth/register` and pass it as `Authorization: Bearer <token>`."
    ),
    version="2.0.0",
    contact={
        "name": "Africa Fintech API Support",
        "url": "https://github.com/Raphasha27/africa-fintech-api",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "User registration, login, and profile management",
        },
        {
            "name": "Wallets",
            "description": "Mobile money wallet operations — create, fund, and query balances",
        },
        {
            "name": "Transactions",
            "description": "Peer-to-peer money transfers and transaction history",
        },
        {"name": "Health", "description": "Service liveness probes"},
    ],
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(wallets.router, prefix="/api/v1")
app.include_router(transactions.router, prefix="/api/v1")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Liveness probe endpoint."""
    return {"status": "ok", "service": "fintech-api"}
