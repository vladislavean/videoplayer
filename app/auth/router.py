import uuid
from datetime import datetime, timezone, timedelta
from app.auth.utils import authenticate_user
from app.database.redis_settings import redis, SESSION_EXPIRE_TIME
from fastapi import APIRouter, Depends, Response, Request


router = APIRouter(tags=["Auth"])


@router.post("/login")
async def login(response: Response, user=Depends(authenticate_user)):
    session_id = str(uuid.uuid4())
    await redis.setex(session_id, SESSION_EXPIRE_TIME, user.id)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,
        expires=datetime.now(timezone.utc) + timedelta(seconds=SESSION_EXPIRE_TIME),
    )
    return response


@router.post("/logout")
async def logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if session_id:
        await redis.delete(session_id)
        response.delete_cookie(key="session_id")
    return {"message": "Logout successful"}

