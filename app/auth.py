from fastapi import Request, HTTPException, Depends
from app.utils import verify_token

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = await verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalid or expired")

    return payload["sub"]