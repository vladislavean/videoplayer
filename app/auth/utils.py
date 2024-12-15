from fastapi import Form, Request, HTTPException
import hashlib
from app.database.models import Users
from app.database.db import get_async_session, find_one_or_none
from app.database.redis_settings import redis


def hash_password(password) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    return hashlib.md5(password.encode()).hexdigest() == hashed_password


async def verify_session(request: Request) -> str:
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")

    user_id = await redis.get(session_id)
    if not user_id:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")

    return user_id


async def authenticate_user(login: str = Form(), password: str = Form()) -> Users | None:
    async with get_async_session() as session:
        user = await find_one_or_none(session=session, model=Users, login=login)
    if not (user and verify_password(password, user.password)):
        return None
    return user
