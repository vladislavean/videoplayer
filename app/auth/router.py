import uuid
from datetime import datetime, timezone, timedelta
from app.auth.utils import authenticate_user
from app.database.models import Users
from app.database.redis_settings import redis, SESSION_EXPIRE_TIME
from fastapi import APIRouter, Depends, Response, Request, HTTPException

auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/login")
async def login(response: Response, user: Users = Depends(authenticate_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Неправильный логин или пароль")
    session_id = str(uuid.uuid4())
    await redis.setex(session_id, SESSION_EXPIRE_TIME, str(user.id))
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        expires=datetime.now(timezone.utc) + timedelta(seconds=SESSION_EXPIRE_TIME),
        samesite=None,
        secure=False,
    )
    return {"message": "Успешный вход в систему"}


@auth_router.post("/logout")
async def logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if session_id:
        await redis.delete(session_id)
        response.delete_cookie(key="session_id")
    return {"message": "Успешный выход из системы"}

