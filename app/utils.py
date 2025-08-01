from jose import jwt
from datetime import datetime, timedelta
import os
from app.redis_client import redis

SECRET_KEY = os.getenv("JWT_SECRET", "devsecret")
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60 * 24

async def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    key = f"access_token:{token}"
    await redis.set(key, data["sub"], ex=EXPIRE_MINUTES * 60)
    return token

async def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        key = f"access_token:{token}"
        user = await redis.get(key)
        if not user:
            return None
        return payload
    except Exception:
        return None
