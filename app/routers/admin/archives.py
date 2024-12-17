import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.database.models import ArchivesTask, Cameras
from app.dependencies import get_auth_admin
from app.database.db import get_async_session, insert_one, update_one, delete_one, find_one_or_none

admin_archives_router = APIRouter(
    prefix='/archives',
    tags=['Admin_Archives_API'],
    dependencies=[Depends(get_auth_admin)]
)


# TODO: сделать загрузку на vps
# @admin_archives_router.post("/upload", summary="Загрузка архива")


@admin_archives_router.post("/add", summary="Создание нового архива")
async def add_archive(name: str, url: str, camera_id: uuid.UUID):
    async with get_async_session() as session:
        camera = await find_one_or_none(session=session, model=Cameras, id=camera_id)
        if not camera:
            raise HTTPException(status_code=404, detail="Камера с таким id не существует")
        return await insert_one(session=session, model=ArchivesTask, name=name, url=url, cameraId=camera_id)


@admin_archives_router.put("/update/{id}", summary="Обновление архива")
async def update_archive(id: uuid.UUID, name: str, url: str, camera_id: uuid.UUID):
    async with get_async_session() as session:
        camera_id = await find_one_or_none(session=session, model=Cameras, id=camera_id)
        if not camera_id:
            raise HTTPException(status_code=404, detail="Камера с таким id не существует")
        return await update_one(session=session, model=ArchivesTask, id=id, name=name, cameraId=camera_id, url=url)


@admin_archives_router.delete("/delete/{id}", summary="Удаление архива")
async def delete_archive(id: uuid.UUID):
    async with get_async_session() as session:
        return await delete_one(session=session, model=ArchivesTask, id=id)
