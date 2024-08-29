from fastapi import HTTPException

from app.api.common.dependencies import bcrypt_context
from app.api.common.utils import create_access_token, create_refresh_token, read_token
from app.dao.users import UsersDAO
from app.dao.refresh_tokens import RefreshTokensDAO
from app.api.routes.auth import helper as auth_helper


def create_new_user(db, body):
    user_model = auth_helper.create_new_user(body)
    _users = UsersDAO(db)
    _refresh_tokens = RefreshTokensDAO(db)

    created_user = _users.create_new_user(user_model)

    access_token = create_access_token(created_user, 'auth')
    refresh_token = create_refresh_token(created_user)

    refresh_token_model = auth_helper.create_new_refresh_token(refresh_token, created_user.id)
    _refresh_tokens.create_new_refresh_token(refresh_token_model)
    return {
        access_token,
        refresh_token
    }


def sign_in(db, body):
    _users = UsersDAO(db)
    _refresh_tokens = RefreshTokensDAO(db)

    user = _users.find_user(body.username)
    if user is None:
        raise HTTPException(status_code=401, detail='Auth failed')
    if not bcrypt_context.verify(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Auth failed')
    access_token = create_access_token(user, 'auth')
    refresh_token = create_refresh_token(user)

    refresh_token_model = auth_helper.create_new_refresh_token(refresh_token, user.id)
    _refresh_tokens.create_new_refresh_token(refresh_token_model)
    return access_token, refresh_token


def new_access_token(db, token):
    _refresh_tokens = RefreshTokensDAO(db)
    _users = UsersDAO(db)

    current_token = _refresh_tokens.get_refresh_token(token)
    if current_token is None:
        raise HTTPException(status_code=401, detail='Auth failed')
    current_user_from_token = read_token(token)
    current_user = _users.find_user(current_user_from_token.get('username'))

    access_token = create_access_token(current_user, 'refresh-token')
    return access_token


def sign_out(db, token):
    payload = read_token(token)
    _refresh_tokens = RefreshTokensDAO(db)

    user_id = payload.get('id')
    _ = _refresh_tokens.delete_token(user_id)













