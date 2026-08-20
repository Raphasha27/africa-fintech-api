from fastapi import APIRouter

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/send")
async def send_money(receiver_id: int, amount: float):
    # Mocking an atomic transaction
    return {"status": "COMPLETED", "transaction_id": "TXN-987654321", "amount": amount}

@router.get("/history")
async def transaction_history():
    return [
        {"id": "TXN-111", "amount": -50.0, "type": "DEBIT", "timestamp": "2024-01-01T10:00:00Z"},
        {"id": "TXN-222", "amount": 200.0, "type": "CREDIT", "timestamp": "2024-01-02T12:30:00Z"}
    ]
