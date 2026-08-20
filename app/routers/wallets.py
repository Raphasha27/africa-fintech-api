from fastapi import APIRouter

router = APIRouter(prefix="/wallets", tags=["Wallets"])

@router.get("/me")
async def get_my_wallet():
    return {"balance": 1500.50, "currency": "ZAR", "status": "ACTIVE"}

@router.post("/topup")
async def topup_wallet(amount: float):
    return {"message": f"Successfully topped up {amount}", "new_balance": 1500.50 + amount}
