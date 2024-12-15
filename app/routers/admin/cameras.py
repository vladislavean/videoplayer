import uuid

from fastapi import APIRouter, Depends

from app.database.db import get_async_session, insert_one, update_one, delete_one
from app.database.models import Cameras
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
