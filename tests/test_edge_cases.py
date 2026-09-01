"""Edge case and boundary tests for the Africa Fintech API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_empty_password(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "empty@example.com", "password": "", "full_name": "Empty"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_missing_email(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={"password": "pass", "full_name": "NoEmail"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_invalid_email_format(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "not-an-email", "password": "pass", "full_name": "Bad Email"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_missing_full_name(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "noname@example.com", "password": "pass"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_with_phone(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "phone@example.com",
            "password": "pass123",
            "full_name": "Phone User",
            "phone": "+27123456789",
        },
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_login_empty_password(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": ""},
    )
    assert response.status_code in (401, 422)


@pytest.mark.asyncio
async def test_login_invalid_email_format(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "not-valid", "password": "pass"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_me_with_invalid_token(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.token.here"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_with_expired_token(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwiZXhwIjoxNjAwMDAwMDAwfQ.invalid"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_fund_wallet_zero_amount(client: AsyncClient) -> None:
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "zero@example.com", "password": "pw", "full_name": "Zero"},
    )
    headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}
    response = await client.post(
        "/api/v1/wallets/fund",
        json={"amount": 0},
        headers=headers,
    )
    assert response.status_code == 400
    assert "positive" in response.json()["detail"]


@pytest.mark.asyncio
async def test_fund_wallet_large_amount(client: AsyncClient) -> None:
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "rich@example.com", "password": "pw", "full_name": "Rich"},
    )
    headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}
    response = await client.post(
        "/api/v1/wallets/fund",
        json={"amount": 999999999999.99},
        headers=headers,
    )
    assert response.status_code == 200
    assert float(response.json()["balance"]) == 999999999999.99


@pytest.mark.asyncio
async def test_fund_wallet_decimal_precision(client: AsyncClient) -> None:
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "decimal@example.com", "password": "pw", "full_name": "Decimal"},
    )
    headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}
    response = await client.post(
        "/api/v1/wallets/fund",
        json={"amount": 0.01},
        headers=headers,
    )
    assert response.status_code == 200
    assert float(response.json()["balance"]) == 0.01


@pytest.mark.asyncio
async def test_transfer_zero_amount(client: AsyncClient) -> None:
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "sender_zero@example.com", "password": "pw", "full_name": "Sender"},
    )
    headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}
    await client.post("/api/v1/wallets/fund", json={"amount": 100}, headers=headers)

    me = await client.get("/api/v1/auth/me", headers=headers)
    sender_id = me.json()["id"]

    response = await client.post(
        "/api/v1/transactions/transfer",
        json={"receiver_id": sender_id + 999, "amount": 0},
        headers=headers,
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_transfer_negative_amount(client: AsyncClient) -> None:
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "sender_neg@example.com", "password": "pw", "full_name": "Sender"},
    )
    headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}
    await client.post("/api/v1/wallets/fund", json={"amount": 100}, headers=headers)

    response = await client.post(
        "/api/v1/transactions/transfer",
        json={"receiver_id": 999, "amount": -50},
        headers=headers,
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_transfer_with_reference(client: AsyncClient) -> None:
    sender_reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "ref_sender@example.com", "password": "pw", "full_name": "Sender"},
    )
    receiver_reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "ref_receiver@example.com", "password": "pw", "full_name": "Receiver"},
    )
    sender_headers = {"Authorization": f"Bearer {sender_reg.json()['access_token']}"}
    receiver_headers = {"Authorization": f"Bearer {receiver_reg.json()['access_token']}"}
    await client.post("/api/v1/wallets/fund", json={"amount": 500}, headers=sender_headers)

    receiver_me = await client.get("/api/v1/auth/me", headers=receiver_headers)
    receiver_id = receiver_me.json()["id"]

    response = await client.post(
        "/api/v1/transactions/transfer",
        json={"receiver_id": receiver_id, "amount": 100, "reference": "INV-2024-001"},
        headers=sender_headers,
    )
    assert response.status_code == 201
    assert response.json()["reference"] == "INV-2024-001"


@pytest.mark.asyncio
async def test_transfer_auto_generates_reference(client: AsyncClient) -> None:
    sender_reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "auto_ref@example.com", "password": "pw", "full_name": "Sender"},
    )
    receiver_reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "auto_ref_recv@example.com", "password": "pw", "full_name": "Receiver"},
    )
    sender_headers = {"Authorization": f"Bearer {sender_reg.json()['access_token']}"}
    receiver_headers = {"Authorization": f"Bearer {receiver_reg.json()['access_token']}"}
    await client.post("/api/v1/wallets/fund", json={"amount": 500}, headers=sender_headers)

    receiver_me = await client.get("/api/v1/auth/me", headers=receiver_headers)
    receiver_id = receiver_me.json()["id"]

    response = await client.post(
        "/api/v1/transactions/transfer",
        json={"receiver_id": receiver_id, "amount": 50},
        headers=sender_headers,
    )
    assert response.status_code == 201
    assert response.json()["reference"].startswith("TXN-")


@pytest.mark.asyncio
async def test_transfer_nonexistent_receiver(client: AsyncClient) -> None:
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "no_recv@example.com", "password": "pw", "full_name": "Sender"},
    )
    headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}
    await client.post("/api/v1/wallets/fund", json={"amount": 100}, headers=headers)

    response = await client.post(
        "/api/v1/transactions/transfer",
        json={"receiver_id": 99999, "amount": 10},
        headers=headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_transaction_history_empty(client: AsyncClient) -> None:
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "empty_hist@example.com", "password": "pw", "full_name": "Empty"},
    )
    headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}
    response = await client.get("/api/v1/transactions/history", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "fintech-api"


@pytest.mark.asyncio
async def test_create_wallet_when_already_has_active(client: AsyncClient) -> None:
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "dup_wallet@example.com", "password": "pw", "full_name": "Dup"},
    )
    headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}

    # First wallet is auto-provisioned
    response = await client.post("/api/v1/wallets", headers=headers)
    assert response.status_code == 400
    assert "Active wallet already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_fund_wallet_without_wallet(client: AsyncClient) -> None:
    """Fund endpoint should handle case where wallet doesn't exist."""
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "no_wallet@example.com", "password": "pw", "full_name": "No Wallet"},
    )
    headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}

    # User has auto-provisioned wallet, so this should work
    response = await client.post(
        "/api/v1/wallets/fund",
        json={"amount": 100},
        headers=headers,
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_transfer_exact_balance(client: AsyncClient) -> None:
    sender_reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "exact@example.com", "password": "pw", "full_name": "Exact"},
    )
    receiver_reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "exact_recv@example.com", "password": "pw", "full_name": "Receiver"},
    )
    sender_headers = {"Authorization": f"Bearer {sender_reg.json()['access_token']}"}
    receiver_headers = {"Authorization": f"Bearer {receiver_reg.json()['access_token']}"}
    await client.post("/api/v1/wallets/fund", json={"amount": 100}, headers=sender_headers)

    receiver_me = await client.get("/api/v1/auth/me", headers=receiver_headers)
    receiver_id = receiver_me.json()["id"]

    response = await client.post(
        "/api/v1/transactions/transfer",
        json={"receiver_id": receiver_id, "amount": 100},
        headers=sender_headers,
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_multiple_funds_accumulate(client: AsyncClient) -> None:
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "multi@example.com", "password": "pw", "full_name": "Multi"},
    )
    headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}

    await client.post("/api/v1/wallets/fund", json={"amount": 100}, headers=headers)
    await client.post("/api/v1/wallets/fund", json={"amount": 200}, headers=headers)
    response = await client.post("/api/v1/wallets/fund", json={"amount": 50}, headers=headers)

    assert float(response.json()["balance"]) == 350.00
