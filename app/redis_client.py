import os
from redis.asyncio import Redis

redis = Redis.from_url(os.getenv("REDIS_URI", "redis://localhost:6379"), decode_responses=True)
