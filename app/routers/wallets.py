"""Wallet management endpoints."""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models import User, Wallet, WalletStatus

router = APIRouter(prefix="/wallets", tags=["Wallets"])


class WalletResponse(BaseModel):
    """Public wallet representation."""

    id: int
    balance: Decimal
    currency: str
    status: WalletStatus

    model_config = {"from_attributes": True}


class FundRequest(BaseModel):
    """Schema for wallet funding."""

    amount: Decimal


@router.get("/me", response_model=WalletResponse)
async def get_my_wallet(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> WalletResponse:
    """Return the authenticated user's wallet."""
    result = await db.execute(
        select(Wallet).where(
            Wallet.user_id == current_user.id, Wallet.status == WalletStatus.ACTIVE
        )
    )
    wallet = result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="No active wallet found")
    return wallet


@router.post("", response_model=WalletResponse, status_code=status.HTTP_201_CREATED)
async def create_wallet(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> WalletResponse:
    """Create a new wallet for the authenticated user."""
    existing = await db.execute(
        select(Wallet).where(
            Wallet.user_id == current_user.id,
            Wallet.status == WalletStatus.ACTIVE,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Active wallet already exists")

    wallet = Wallet(user_id=current_user.id, currency="USD")
    db.add(wallet)
    await db.flush()
    return wallet


@router.post("/fund", response_model=WalletResponse)
async def fund_wallet(
    request: FundRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> WalletResponse:
    """Fund the authenticated user's wallet (deposit)."""
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    result = await db.execute(
        select(Wallet).where(
            Wallet.user_id == current_user.id, Wallet.status == WalletStatus.ACTIVE
        )
    )
    wallet = result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="No active wallet found")

    wallet.balance = Decimal(str(wallet.balance)) + request.amount
    return wallet
