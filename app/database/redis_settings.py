from redis import asyncio as aioredis

from app.database.settings import api_settings


redis = aioredis.StrictRedis(
    host=api_settings.REDIS_HOST,
    port=api_settings.REDIS_PORT,
    decode_responses=True
)

SESSION_EXPIRE_TIME = 3600 * 24 * 7
