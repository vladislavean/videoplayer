import uuid
from fastapi import APIRouter, Depends, Form, Request
from app.database.db import select_all, find_all, get_async_session, find_one_or_none
from app.database.models import Cameras
from app.database.schemas import SchemaCamera
from app.dependencies import get_auth_user

cameras_router = APIRouter(
    prefix='/cameras',
    tags=['Cameras_API'],
    dependencies=[Depends(get_auth_user)]
)


@cameras_router.get(
    "/",
    response_model=list[SchemaCamera],
    summary="Все камеры",
)
async def get_cameras(request: Request):
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Headers: {request.headers}")
    print(f"Query params: {request.query_params}")
    print(f"Body: {request.body}")
    print(f"Cookies: {request.cookies}")
    async with get_async_session() as session:
        return await select_all(session=session, model=Cameras)


@cameras_router.get(
    "/{id}",
    response_model=SchemaCamera,
    summary="Найти камеру по id",
)
async def get_camera_by_id(id: uuid.UUID):
    async with get_async_session() as session:
        return await find_one_or_none(session=session, model=Cameras, id=id)


@cameras_router.get(
    "/by_street/{street_id}",
    response_model=list[SchemaCamera],
    summary="Найти камеры по id улицы",
)
async def get_cameras_by_street(street_id: uuid.UUID):
    async with get_async_session() as session:
        return await find_all(session=session, model=Cameras, streetId=street_id)