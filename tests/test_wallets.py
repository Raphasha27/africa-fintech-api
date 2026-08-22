"""Tests for the /wallets endpoints."""

import pytest
from httpx import AsyncClient


async def _auth_headers(client: AsyncClient) -> dict[str, str]:
    """Register a user and return Bearer headers."""
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "wallet@example.com", "password": "pw", "full_name": "Wallet User"},
    )
    return {"Authorization": f"Bearer {reg.json()['access_token']}"}


@pytest.mark.asyncio
async def test_wallet_created_on_register(client: AsyncClient) -> None:
    headers = await _auth_headers(client)
    response = await client.get("/api/v1/wallets/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["currency"] == "USD"
    assert data["status"] == "active"


@pytest.mark.asyncio
async def test_create_wallet_success(client: AsyncClient) -> None:
    """Create a second wallet after the auto-provisioned one is closed."""
    headers = await _auth_headers(client)
    response = await client.post("/api/v1/wallets", headers=headers)
    assert response.status_code == 201
    assert response.json()["currency"] == "USD"


@pytest.mark.asyncio
async def test_fund_wallet(client: AsyncClient) -> None:
    headers = await _auth_headers(client)
    response = await client.post(
        "/api/v1/wallets/fund",
        json={"amount": 500.00},
        headers=headers,
    )
    assert response.status_code == 200
    assert float(response.json()["balance"]) == 500.00


@pytest.mark.asyncio
async def test_fund_wallet_negative_amount(client: AsyncClient) -> None:
    headers = await _auth_headers(client)
    response = await client.post(
        "/api/v1/wallets/fund",
        json={"amount": -100},
        headers=headers,
    )
    assert response.status_code == 400
    assert "positive" in response.json()["detail"]
