from fastapi import APIRouter

from app.api.routes.auth import handler as auth_handler
from app.api.routes.boards import handler as boards_handler

router = APIRouter()


@router.get("/health")
async def app_health_check():
    return {"data": "You are accessing task-orbit API"}


router.include_router(auth_handler.router, prefix="/auth", tags=["/auth"])
router.include_router(boards_handler.router, prefix="/boards", tags=["/boards"])
