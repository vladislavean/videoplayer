import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.database.models import FunctionalRoles
from app.dependencies import get_auth_admin
from app.database.db import (
    get_async_session, select_all, find_one_or_none, find_all, insert_one, update_one, delete_one
)


admin_roles_router = APIRouter(
    prefix="/roles",
    tags=["Admin_Roles_API"],
    dependencies=[Depends(get_auth_admin)]
)


@admin_roles_router.get("/", summary="Все роли")
async def get_roles():
    async with get_async_session() as session:
        return await select_all(session=session, model=FunctionalRoles)


@admin_roles_router.get("/{role_id}", summary="Найти роли по id")
async def get_role_by_id(role_id: uuid.UUID):
    async with get_async_session() as session:
        return await find_one_or_none(session=session, model=FunctionalRoles, id=role_id)


@admin_roles_router.post("/add", summary="Создание новой роли")
async def add_role(role_name: str):
    async with get_async_session() as session:
        role = await find_one_or_none(session=session, model=FunctionalRoles, name=role_name)
        if role:
            raise HTTPException(status_code=400, detail="Роль с таким названием уже существует")
        return await insert_one(session=session, model=FunctionalRoles, name=role_name)


@admin_roles_router.put("/update/{id}", summary="Обновление роли")
async def update_role(id: uuid.UUID, name: str):
    async with get_async_session() as session:
        role = await find_one_or_none(session=session, model=FunctionalRoles, name=name)
        if role.id != id:
            raise HTTPException(status_code=400, detail="Роль с таким названием уже существует")
        return await update_one(session=session, model=FunctionalRoles, id=id, name=name)


@admin_roles_router.delete("/delete/{id}", summary="Удаление роли")
async def delete_role(id: uuid.UUID):
    async with get_async_session() as session:
        return await delete_one(session=session, model=FunctionalRoles, id=id)