import uuid
from fastapi import APIRouter
from app.database.db import select_all, find_all, insert_one, get_async_session
from app.database.models import Cameras
from app.database.schemas import SchemaCamera


cameras_router = APIRouter(prefix='/cameras', tags=['Cameras_API'])


@cameras_router.get(
    "/",
    response_model=list[SchemaCamera],
    summary="Все камеры",
)
async def get_cameras():
    async with get_async_session() as session:
        return await select_all(session=session, model=Cameras)


@cameras_router.get(
    "/{street_id}",
    response_model=list[SchemaCamera],
    summary="Найти камеры по id улицы",
)
async def get_cameras_by_street(street_id: uuid.UUID):
    async with get_async_session() as session:
        return await find_all(session=session, model=Cameras, streetId=street_id)


@cameras_router.post(
    "/add",
    summary="Добавление новой камеры на портал. Id улицы указывать самостоятельно пж",
)
async def add_camera(
    camera_title: str,
    camera_streetid: uuid.UUID,
    camera_address: str
):
    async with get_async_session() as session:
        return await insert_one(
            session=session,
            model=Cameras,
            title=camera_title,
            streetId=camera_streetid,
            address=camera_address
        )