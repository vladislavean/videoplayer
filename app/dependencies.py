from fastapi import Request, Depends, HTTPException
from app.database.db import get_async_session, find_one_or_none
from app.database.models import Users, FunctionalRoles

from app.database.redis_settings import redis


async def get_current_user(request: Request) -> str:
    session = str(request.cookies.get("session_id"))
    if not session:
        raise HTTPException(status_code=401, detail="Вы не авторизованы (сессия истекла)")
    user_id = await redis.get(session)
    if not user_id:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")
    return user_id


async def get_auth_user(user_id: str = Depends(get_current_user)) -> Users:
    if not user_id:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")
    async with get_async_session() as session:
        user = await find_one_or_none(session=session, model=Users, id=str(user_id))
        if not user:
            raise HTTPException(status_code=401, detail="Вы не авторизованы")
        return user


async def get_auth_admin(user_id: str = Depends(get_current_user)) -> Users:
    if not user_id:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")
    async with get_async_session() as session:
        user = await find_one_or_none(session=session, model=Users, id=user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Вы не авторизованы")
        role = await find_one_or_none(session=session, model=FunctionalRoles, id=user.roleId)
        if not role:
            raise HTTPException(status_code=401, detail="Вы не авторизованы")
        if role.name != "admin":
            raise HTTPException(status_code=401, detail="У вас нет доступа")
        return user



