from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.core.security import verify_admin_password, create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """
    Admin login endpoint - verifies password and returns JWT token.
    Use the provided password to access protected endpoints.
    """
    if not verify_admin_password(login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": "admin", "role": "admin"})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )

@router.post("/verify", response_model=dict)
async def verify_token():
    """
    Endpoint to verify if the current token is valid.
    This will be protected by the auth dependency.
    """
    return {"valid": True, "message": "Token is valid"}
