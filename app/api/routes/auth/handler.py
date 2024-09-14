from fastapi import APIRouter
from starlette import status

from app.api.common.dependencies import db_dependency, token_dependency
from app.api.routes.auth import schema as auth_schema
from app.api.routes.auth import service as auth_service

router = APIRouter()


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_new_user(db: db_dependency, body: auth_schema.CreateNewUser):
    token, refresh_token = auth_service.create_new_user(db=db, body=body)
    return {
        "data": {"access_token": token, "refresh_token": refresh_token},
        "message": "user signed up successfully",
    }


@router.post("/sign-in", status_code=status.HTTP_200_OK)
async def sign_in(
    db: db_dependency,
    body: auth_schema.SignIn,
):
    access_token, refresh_token = auth_service.sign_in(db=db, body=body)
    return {
        "data": {"access_token": access_token, "refresh_token": refresh_token},
        "message": "sign in success",
    }


@router.get("/refresh-token", status_code=status.HTTP_200_OK)
async def new_refresh_token(db: db_dependency, token: token_dependency):
    access_token = auth_service.new_access_token(db=db, token=token.credentials)
    return {"data": {"access_token": access_token}, "message": "new access token"}


@router.post("/sign-out", status_code=status.HTTP_200_OK)
async def sign_out(db: db_dependency, token: token_dependency):
    _ = auth_service.sign_out(db, token=token.credentials)
