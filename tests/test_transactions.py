"""Tests for the /transactions endpoints."""

import pytest
from httpx import AsyncClient


async def _register_and_fund(client: AsyncClient, email: str, amount: float = 1000.0) -> str:
    """Register a user, fund their wallet, return the JWT token."""
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "pw", "full_name": "Txn User"},
    )
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    await client.post(
        "/api/v1/wallets/fund",
        json={"amount": amount},
        headers=headers,
    )
    return token


@pytest.mark.asyncio
async def test_transfer_success(client: AsyncClient) -> None:
    sender_token = await _register_and_fund(client, "sender@example.com")
    receiver_token = await _register_and_fund(client, "receiver@example.com")

    receiver_me = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {receiver_token}"},
    )
    receiver_id = receiver_me.json()["id"]

    response = await client.post(
        "/api/v1/transactions/transfer",
        json={"receiver_id": receiver_id, "amount": 250.00},
        headers={"Authorization": f"Bearer {sender_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "completed"
    assert float(data["amount"]) == 250.00


@pytest.mark.asyncio
async def test_transfer_insufficient_funds(client: AsyncClient) -> None:
    sender_token = await _register_and_fund(client, "poor@example.com", amount=10.0)
    receiver_token = await _register_and_fund(client, "rich@example.com")

    receiver_me = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {receiver_token}"},
    )
    receiver_id = receiver_me.json()["id"]

    response = await client.post(
        "/api/v1/transactions/transfer",
        json={"receiver_id": receiver_id, "amount": 999.99},
        headers={"Authorization": f"Bearer {sender_token}"},
    )
    assert response.status_code == 402
    assert "Insufficient" in response.json()["detail"]


@pytest.mark.asyncio
async def test_transfer_to_self(client: AsyncClient) -> None:
    token = await _register_and_fund(client, "self@example.com")
    me = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    my_id = me.json()["id"]

    response = await client.post(
        "/api/v1/transactions/transfer",
        json={"receiver_id": my_id, "amount": 10},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert "yourself" in response.json()["detail"]


@pytest.mark.asyncio
async def test_transaction_history(client: AsyncClient) -> None:
    token = await _register_and_fund(client, "history@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    me = await client.get("/api/v1/auth/me", headers=headers)
    receiver_id = me.json()["id"]

    await client.post(
        "/api/v1/auth/register",
        json={"email": "hist-sender@example.com", "password": "pw", "full_name": "Sender"},
    )
    sender_login = await client.post(
        "/api/v1/auth/login",
        json={"email": "hist-sender@example.com", "password": "pw"},
    )
    sender_headers = {"Authorization": f"Bearer {sender_login.json()['access_token']}"}
    await client.post(
        "/api/v1/wallets/fund",
        json={"amount": 500},
        headers=sender_headers,
    )
    await client.post(
        "/api/v1/transactions/transfer",
        json={"receiver_id": receiver_id, "amount": 100},
        headers=sender_headers,
    )

    response = await client.get("/api/v1/transactions/history", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1
