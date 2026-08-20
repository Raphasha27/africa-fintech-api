from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register():
    return {"message": "User registered and wallet auto-created"}

@router.post("/login")
async def login():
    return {"access_token": "mock_jwt_token", "token_type": "bearer"}
