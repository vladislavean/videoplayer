from fastapi import APIRouter
from app.database.db import select_all, insert_one, get_async_session
from app.database.models import Streets
from app.database.schemas import SchemaStreet


streets_router = APIRouter(prefix='/streets', tags=['Street_API'])


@streets_router.get(
    "/",
    response_model=list[SchemaStreet],
    summary="Все улицы",
    tags=['Street_API']
)
async def get_streets():
    async with get_async_session() as session:
        return await select_all(session=session, model=Streets)


@streets_router.post("/add", summary="Создание новой улицы")
async def add_street(street_name: str):
    async with get_async_session() as session:
        return await insert_one(session=session, model=Streets, name=street_name)