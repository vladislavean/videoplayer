from fastapi import APIRouter, Depends
from app.dependencies import get_auth_admin


admin_archives_router = APIRouter(
    prefix='/archives',
    tags=['Admin_Archives_API'],
    dependencies=[Depends(get_auth_admin)]
)