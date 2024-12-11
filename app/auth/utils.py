from fastapi import Form, status, Request
import hashlib
from app.database.models import Users
from app.database.db import get_async_session, find_one_or_none
from app.database.redis_settings import redis


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    return hashlib.md5(password.encode()).hexdigest() == hashed_password


async def verify_session(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        return status.HTTP_401_UNAUTHORIZED(detail="Вы не авторизованы")

    user_id = await redis.get(session_id)
    if not user_id:
        return status.HTTP_401_UNAUTHORIZED(detail="Вы не авторизованы")

    return {"user_id": user_id}


async def authenticate_user(login: str = Form(), password: str = Form()):
    async with get_async_session() as session:
        user = await find_one_or_none(session=session, model=Users, login=login)
    if not (user and verify_password(password, user.password)):
        return None
    return user
