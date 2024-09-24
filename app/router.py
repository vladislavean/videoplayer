import uuid
from fastapi import HTTPException

from fastapi import APIRouter

from app.database.db import select_all, find_all, find_one_or_none
from app.database.models import Streets, Cameras, ArchivesTask
from app.utils import download_video

router = APIRouter()


@router.get("/")
async def get_streets():
    return await select_all(Streets)


@router.get("/cameras")
async def get_cameras():
    return await select_all(Cameras)


@router.get("/archives")
async def get_archives():
    return await select_all(ArchivesTask)


@router.get("/cameras/{street_id}")
async def get_cameras_by_street(street_id: uuid.UUID):
    return await find_all(Cameras, streetId=street_id)


@router.get("/archives/{camera_id}")
async def get_archives_by_camera(camera_id: uuid.UUID):
    return await find_all(ArchivesTask, cameraId=camera_id)


@router.get("/archive/{archive_id}")
async def get_archive_video(archive_id: uuid.UUID):
    archive = await find_one_or_none(ArchivesTask, id=archive_id)
    if archive is None:
        raise HTTPException(status_code=404)
    return await download_video(archive.url)
