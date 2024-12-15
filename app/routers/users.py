from fastapi import APIRouter, Depends, Form, HTTPException
from app.dependencies import get_auth_user
from app.database.db import get_async_session, find_one_or_none, update_one
from app.database.models import Users, FunctionalRoles
from app.auth.utils import hash_password, verify_password


users_router = APIRouter(
    prefix='/users',
    tags=['Users_API'],
)


@users_router.get("/me", summary="Мои данные")
async def get_me(user: Users = Depends(get_auth_user)):
    async with get_async_session() as session:
        role = await find_one_or_none(session=session, model=FunctionalRoles, id=user.roleId)
    return {
        "login": user.login,
        "fio": user.fio,
        "role": role.name,
    }


@users_router.put("/update_login", summary="Обновление логина")
async def update_login(
        old_login: str = Form(),
        new_login: str = Form(),
        user: Users = Depends(get_auth_user)):
    async with get_async_session() as session:
        if old_login != user.login:
            raise HTTPException(status_code=401, detail="Неправильный логин")
        if new_login == old_login:
            raise HTTPException(status_code=400, detail="Новый логин должен отличаться от старого")
        user_exist = await find_one_or_none(session=session, model=Users, login=new_login)
        if user_exist.id != user.id:
            raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует")
        return await update_one(session=session, model=Users, id=user.id, login=new_login)


@users_router.put("/update_password", summary="Обновление пароля")
async def update_password(
        old_password: str = Form(),
        new_password: str = Form(),
        user: Users = Depends(get_auth_user)
):
    if not verify_password(old_password, user.password):
        raise HTTPException(status_code=401, detail="Неправильный пароль")
    async with get_async_session() as session:
        return await update_one(
            session=session,
            model=Users,
            id=user.id,
            password=hash_password(new_password)
        )

