import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.database.db import get_async_session, insert_one, update_one, delete_one, find_one_or_none
from app.database.models import Streets
from app.dependencies import get_auth_admin


admin_streets_router = APIRouter(
    prefix='/streets',
    tags=['Admin_Streets_API'],
    dependencies=[Depends(get_auth_admin)]
)


@admin_streets_router.post("/add", summary="Создание новой улицы")
async def add_street(street_name: str):
    async with get_async_session() as session:
        street = await find_one_or_none(session=session, model=Streets, name=street_name)
        if street:
            raise HTTPException(status_code=400, detail="Улица с таким названием уже существует")
        return await insert_one(session=session, model=Streets, name=street_name)


@admin_streets_router.put("/update/{id}", summary="Обновление улицы")
async def update_street(id: uuid.UUID, name: str):
    async with get_async_session() as session:
        street = await find_one_or_none(session=session, model=Streets, name=name)
        if street.id != id:
            raise HTTPException(status_code=400, detail="Улица с таким названием уже существует")
        return await update_one(session=session, model=Streets, id=id, name=name)


@admin_streets_router.delete("/delete/{id}", summary="Удаление улицы")
async def delete_street(id: uuid.UUID):
    async with get_async_session() as session:
        return await delete_one(session=session, model=Streets, id=id)
