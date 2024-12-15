import uuid

from fastapi import APIRouter, Depends, Form

from app.database.models import Users
from app.dependencies import get_auth_admin
from app.database.db import (
    get_async_session, select_all, find_one_or_none, find_all, insert_one, update_one, delete_one
)
from app.auth.utils import hash_password

admin_users_router = APIRouter(
    prefix="/users",
    tags=["Admin_Users_API"],
    dependencies=[Depends(get_auth_admin)]
)


@admin_users_router.get("/", summary="Все пользователи")
async def get_all_users():
    async with get_async_session() as session:
        return await select_all(session=session, model=Users)


@admin_users_router.get("/{user_id}", summary="Найти пользователя по id")
async def get_user_by_id(user_id: uuid.UUID):
    async with get_async_session() as session:
        return await find_one_or_none(session=session, model=Users, id=user_id)


@admin_users_router.get("/{role_id}", summary="Найти пользователей по id роли")
async def get_users_by_role_id(role_id: uuid.UUID):
    async with get_async_session() as session:
        return await find_all(session=session, model=Users, roleId=role_id)


@admin_users_router.post("/add", summary="Создание нового пользователя")
async def add_user(
    user_login: str,
    user_password: str,
    user_fio: str,
    user_roleId: uuid.UUID,
):
    async with get_async_session() as session:
        return await insert_one(
            session=session,
            model=Users,
            login=user_login,
            password=hash_password(user_password),
            fio=user_fio,
            roleId=user_roleId
        )
