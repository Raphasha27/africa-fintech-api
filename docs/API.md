# Africa Fintech API — Documentation

> Production-grade mobile money and remittance backend for African fintech markets.

## Base URL

```
http://localhost:8000
```

## Authentication

All protected endpoints require a JWT Bearer token. Include it in the `Authorization` header:

```
Authorization: Bearer <your-token>
```

Obtain a token via the [Register](#register) or [Login](#login) endpoints.

---

## Endpoints

### Health

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness probe |

### Authentication

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/auth/register` | Register a new user (auto-provisions a wallet) |
| `POST` | `/api/v1/auth/login` | Login and receive a JWT token |
| `GET` | `/api/v1/auth/me` | Get current user profile *(auth required)* |

### Wallets

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/wallets` | Create a new wallet *(auth required)* |
| `GET` | `/api/v1/wallets/me` | Get my active wallet *(auth required)* |
| `POST` | `/api/v1/wallets/fund` | Fund (deposit to) wallet *(auth required)* |

### Transactions

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/transactions/transfer` | Peer-to-peer money transfer *(auth required)* |
| `GET` | `/api/v1/transactions/history` | Transaction history *(auth required)* |

---

## Example Requests

### Register

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secureP@ss123",
    "full_name": "Jane Doe",
    "phone": "+254700123456"
  }'
```

**Response (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secureP@ss123"
  }'
```

### Get My Wallet

```bash
curl http://localhost:8000/api/v1/wallets/me \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "id": 1,
  "balance": 15000.00,
  "currency": "USD",
  "status": "ACTIVE"
}
```

### Fund Wallet

```bash
curl -X POST http://localhost:8000/api/v1/wallets/fund \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 5000.00}'
```

### Transfer Money

```bash
curl -X POST http://localhost:8000/api/v1/transactions/transfer \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_id": 2,
    "amount": 100.00,
    "reference": "Payment for services"
  }'
```

**Response (201):**
```json
{
  "id": 1,
  "wallet_id": 1,
  "type": "TRANSFER",
  "amount": 100.00,
  "status": "COMPLETED",
  "reference": "TXN-A1B2C3D4E5F6",
  "created_at": "2025-01-15 10:30:00"
}
```

### Transaction History

```bash
curl http://localhost:8000/api/v1/transactions/history \
  -H "Authorization: Bearer <token>"
```

---

## Interactive Docs

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Spec:** [`docs/api-spec.yaml`](./api-spec.yaml)
