import uuid

from fastapi import APIRouter, Depends, Request
from app.dependencies import get_auth_user
from app.database.db import select_all, get_async_session, find_one_or_none
from app.database.models import Streets
from app.database.schemas import SchemaStreet


streets_router = APIRouter(
    prefix='/streets',
    tags=['Street_API'],
    dependencies=[Depends(get_auth_user)],
)


@streets_router.get(
    "/",
    response_model=list[SchemaStreet],
    summary="Все улицы",
)
async def get_streets(request: Request):
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Headers: {request.headers}")
    print(f"Query params: {request.query_params}")
    print(f"Body: {request.body}")
    print(f"Cookies: {request.cookies}")
    async with get_async_session() as session:
        return await select_all(session=session, model=Streets)


@streets_router.get(
    "/{id}",
    response_model=SchemaStreet,
    summary="Найти улицу по id",
)
async def get_street_by_id(id: uuid.UUID):
    async with get_async_session() as session:
        return await find_one_or_none(session=session, model=Streets, id=id)


