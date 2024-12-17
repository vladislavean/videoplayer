import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from app.database.db import select_all, find_all, find_one_or_none, get_async_session
from app.database.models import ArchivesTask
from app.database.schemas import SchemaArchiveTask
from app.dependencies import get_auth_user
from app.utils import streaming_video, download_video

archives_router = APIRouter(
    prefix='/archives',
    tags=['Archives_API'],
    dependencies=[Depends(get_auth_user)]
)


@archives_router.get(
    "/",
    response_model=list[SchemaArchiveTask],
    summary="Все видосы",
)
async def get_archives(request: Request):
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Headers: {request.headers}")
    print(f"Query params: {request.query_params}")
    async with get_async_session() as session:
        return await select_all(session=session, model=ArchivesTask)


@archives_router.get(
    "/{archive_id}",
    response_model=SchemaArchiveTask,
    summary="Найти видос по id",
)
async def get_archive_by_id(archive_id: uuid.UUID):
    async with get_async_session() as session:
        return await find_one_or_none(session=session, model=ArchivesTask, id=archive_id)


@archives_router.get(
    "/by_camera/{camera_id}",
    response_model=list[SchemaArchiveTask],
    summary="Найти видосы по id камеры",
)
async def get_archives_by_camera(camera_id: uuid.UUID):
    async with get_async_session() as session:
        return await find_all(session=session, model=ArchivesTask, cameraId=camera_id)


@archives_router.get(
    "/watch/{archive_id}",
    summary="Стрим видоса по id (чистые байты)",
)
async def get_archive_video(archive_id: uuid.UUID):
    async with get_async_session() as session:
        archive = await find_one_or_none(session=session, model=ArchivesTask, id=archive_id)
    if archive is None:
        raise HTTPException(status_code=404)
    return await streaming_video(archive.url)


@archives_router.get(
    "/download/{archive_id}",
    summary="Скачивание видео",
)
async def get_archive_video(archive_id: uuid.UUID):
    async with get_async_session() as session:
        archive = await find_one_or_none(session=session, model=ArchivesTask, id=archive_id)
    if archive is None:
        raise HTTPException(status_code=404)
    return await download_video(archive.url, archive_id)