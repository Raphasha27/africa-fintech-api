"""SQLAlchemy ORM models for the Africa Fintech API."""

import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class TransactionType(str, enum.Enum):
    """Supported transaction types."""

    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"


class TransactionStatus(str, enum.Enum):
    """Transaction lifecycle statuses."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class WalletStatus(str, enum.Enum):
    """Wallet statuses."""

    ACTIVE = "active"
    FROZEN = "frozen"
    CLOSED = "closed"


class User(Base):
    """User account model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    wallets = relationship("Wallet", back_populates="user", cascade="all, delete-orphan")


class Wallet(Base):
    """Digital wallet model with multi-currency support."""

    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    balance = Column(Numeric(15, 2), default=Decimal("0.00"), nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    status: Mapped[WalletStatus] = Column(Enum(WalletStatus), default=WalletStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="wallets")
    transactions = relationship(
        "Transaction", back_populates="wallet", cascade="all, delete-orphan"
    )


class Transaction(Base):
    """Transaction record model."""

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[TransactionType] = Column(Enum(TransactionType), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    status: Mapped[TransactionStatus] = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING, nullable=False)
    reference = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    wallet = relationship("Wallet", back_populates="transactions")
