from fastapi import Header, HTTPException, Depends
from app.core.config import settings


def verify_api_key(x_api_key: str = Header()):

    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    return x_api_key



def get_current_user(
    api_key: str = Depends(verify_api_key)
):
    return {
        "username": "ali",
        "role": "user"
    }
    
    
def require_admin(
    user: dict = Depends(get_current_user)
):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user