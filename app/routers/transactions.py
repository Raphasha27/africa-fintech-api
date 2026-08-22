"""Transaction endpoints: transfers and history."""

import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models import Transaction, TransactionStatus, TransactionType, User, Wallet, WalletStatus

router = APIRouter(prefix="/transactions", tags=["Transactions"])


class TransferRequest(BaseModel):
    """Schema for P2P money transfer."""

    receiver_id: int
    amount: Decimal
    reference: str | None = None


class TransactionResponse(BaseModel):
    """Public transaction representation."""

    id: int
    wallet_id: int
    type: TransactionType
    amount: Decimal
    status: TransactionStatus
    reference: str | None
    created_at: str

    model_config = {"from_attributes": True}


@router.post("/transfer", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def transfer_money(
    request: TransferRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TransactionResponse:
    """Transfer money from the sender's wallet to a receiver's wallet."""
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    if request.receiver_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot transfer to yourself")

    sender_result = await db.execute(
        select(Wallet).where(Wallet.user_id == current_user.id, Wallet.status == WalletStatus.ACTIVE)
    )
    sender_wallet = sender_result.scalar_one_or_none()
    if not sender_wallet:
        raise HTTPException(status_code=404, detail="Sender wallet not found")

    if Decimal(str(sender_wallet.balance)) < request.amount:
        raise HTTPException(status_code=402, detail="Insufficient funds")

    receiver_result = await db.execute(
        select(Wallet).where(Wallet.user_id == request.receiver_id, Wallet.status == WalletStatus.ACTIVE)
    )
    receiver_wallet = receiver_result.scalar_one_or_none()
    if not receiver_wallet:
        raise HTTPException(status_code=404, detail="Receiver wallet not found")

    reference = request.reference or f"TXN-{uuid.uuid4().hex[:12].upper()}"

    sender_wallet.balance = Decimal(str(sender_wallet.balance)) - request.amount
    receiver_wallet.balance = Decimal(str(receiver_wallet.balance)) + request.amount

    txn = Transaction(
        wallet_id=sender_wallet.id,
        type=TransactionType.TRANSFER,
        amount=request.amount,
        status=TransactionStatus.COMPLETED,
        reference=reference,
    )
    db.add(txn)
    await db.flush()

    return TransactionResponse(
        id=txn.id,
        wallet_id=txn.wallet_id,
        type=txn.type,
        amount=txn.amount,
        status=txn.status,
        reference=txn.reference,
        created_at=str(txn.created_at),
    )


@router.get("/history", response_model=list[TransactionResponse])
async def transaction_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[TransactionResponse]:
    """Return the transaction history for the authenticated user's wallet."""
    wallet_result = await db.execute(
        select(Wallet).where(Wallet.user_id == current_user.id, Wallet.status == WalletStatus.ACTIVE)
    )
    wallet = wallet_result.scalar_one_or_none()
    if not wallet:
        return []

    result = await db.execute(
        select(Transaction)
        .where(Transaction.wallet_id == wallet.id)
        .order_by(Transaction.created_at.desc())
        .limit(50)
    )
    transactions = result.scalars().all()
    return [
        TransactionResponse(
            id=t.id,
            wallet_id=t.wallet_id,
            type=t.type,
            amount=t.amount,
            status=t.status,
            reference=t.reference,
            created_at=str(t.created_at),
        )
        for t in transactions
    ]
