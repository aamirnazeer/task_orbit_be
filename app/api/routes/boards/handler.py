from fastapi import APIRouter
from starlette import status

from app.api.common.dependencies import db_dependency, token_dependency
from app.api.routes.boards import schema as boards_schema
from app.api.routes.boards import service as boards_service

router = APIRouter()


@router.post("/create-board", status_code=status.HTTP_201_CREATED)
async def create_new_board(
    db: db_dependency, body: boards_schema.CreateNewBoard, token: token_dependency
):
    board = boards_service.create_new_board(db=db, body=body, token=token.credentials)
    return {
        "data": board,
        "message": "board added successfully",
    }
