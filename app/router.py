from fastapi import APIRouter

from app.database.db import select_all
from app.database.models import Streets

router = APIRouter()


@router.get("/")
async def get_streets():
    return await select_all(Streets)


@router.get("/cameras")
async def get_cameras():
    pass


