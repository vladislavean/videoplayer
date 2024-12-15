import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.database.db import get_async_session, insert_one, update_one, delete_one, find_one_or_none
from app.database.models import Cameras, Streets
from app.dependencies import get_auth_admin


admin_cameras_router = APIRouter(
    prefix='/cameras',
    tags=['Admin_Cameras_API'],
    dependencies=[Depends(get_auth_admin)]
)


@admin_cameras_router.post(
    "/add",
    summary="Добавление новой камеры на портал. Id улицы указывать самостоятельно пж",
)
async def add_camera(
    camera_title: str,
    camera_streetId: uuid.UUID,
    camera_address: str
):
    async with get_async_session() as session:
        street = await find_one_or_none(session=session, model=Streets, id=camera_streetId)
        if not street:
            raise HTTPException(status_code=404, detail="Улица с таким id не существует")

        return await insert_one(
            session=session,
            model=Cameras,
            title=camera_title,
            streetId=camera_streetId,
            address=camera_address
        )


@admin_cameras_router.put("/update/{id}", summary="Обновление камеры")
async def update_camera(
        id: uuid.UUID,
        camera_title: str,
        camera_streetId: uuid.UUID,
        camera_address: str,
):
    async with get_async_session() as session:
        street = await find_one_or_none(session=session, model=Streets, id=camera_streetId)
        if not street:
            raise HTTPException(status_code=404, detail="Улица с таким id не существует")

        return await update_one(
            session=session,
            model=Cameras,
            id=id,
            title=camera_title,
            streetId=camera_streetId,
            address=camera_address
        )


@admin_cameras_router.delete("/delete/{id}", summary="Удаление камеры")
async def delete_camera(id: uuid.UUID):
    async with get_async_session() as session:
        return await delete_one(session=session, model=Cameras, id=id)
