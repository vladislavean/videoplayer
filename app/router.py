import uuid
from fastapi import HTTPException

from fastapi import APIRouter

from app.database.db import select_all, find_all, find_one_or_none, insert_one
from app.database.models import Streets, Cameras, ArchivesTask
from app.database.schemas import SchemaStreet, SchemaCamera, SchemaArchiveTask
from app.utils import streaming_video, download_video

router = APIRouter()


@router.get(
    "/",
    response_model=list[SchemaStreet],
    summary="Все улицы",
    tags=['Street_API']
)
async def get_streets():
    return await select_all(Streets)


@router.get(
    "/cameras",
    response_model=list[SchemaCamera],
    summary="Все камеры",
    tags=['Cameras_API']
)
async def get_cameras():
    return await select_all(Cameras)


@router.get(
    "/archives",
    response_model=list[SchemaArchiveTask],
    summary="Все видосы",
    tags=['Archives_API']
)
async def get_archives():
    return await select_all(ArchivesTask)


@router.get(
    "/cameras/{street_id}",
    response_model=list[SchemaCamera],
    summary="Найти камеры по id улицы",
    tags=['Cameras_API']
)
async def get_cameras_by_street(street_id: uuid.UUID):
    return await find_all(Cameras, streetId=street_id)


@router.get(
    "/archives/{camera_id}",
    response_model=list[SchemaArchiveTask],
    summary="Найти видосы по id камеры",
    tags=['Archives_API']
)
async def get_archives_by_camera(camera_id: uuid.UUID):
    return await find_all(ArchivesTask, cameraId=camera_id)


@router.get(
    "/archive/{archive_id}",
    summary="Стрим видоса по id (чистые байты)",
    tags=['Archives_API']
)
async def get_archive_video(archive_id: uuid.UUID):
    archive = await find_one_or_none(ArchivesTask, id=archive_id)
    if archive is None:
        raise HTTPException(status_code=404)
    return await streaming_video(archive.url)


@router.get(
    "/archive/download/{archive_id}",
    summary="Скачивание видео",
    tags=['Archives_API']
)
async def get_archive_video(archive_id: uuid.UUID):
    archive = await find_one_or_none(ArchivesTask, id=archive_id)
    if archive is None:
        raise HTTPException(status_code=404)
    return await download_video(archive.url, archive_id)


@router.post("/street",
             summary="Создание новой улицы",
             tags=['Street_API'])
async def add_street(street_name: str):
    return await insert_one(Streets, name=street_name)


@router.post(
    "/camera",
    summary="Добавление новой камеры на портал. Id улицы указывать самостоятельно пж",
    tags=['Cameras_API']
)
async def add_camera(camera_title: str,
                     camera_streetid: uuid.UUID,
                     camera_address: str):
    return await insert_one(Cameras, title=camera_title, streetid=camera_streetid, address=camera_address)
