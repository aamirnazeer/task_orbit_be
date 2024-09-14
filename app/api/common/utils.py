import os
from time import time
from typing import Annotated
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.env import SECRET_KEY, ALGORITHM
from app.models.users import Users


security = HTTPBearer()


def create_access_token(created_user: Users, origin: str):
    encode = {
        "username": created_user.username,
        "id": created_user.id,
        "role": created_user.role,
        "origin": origin,
    }
    expires = int(time()) + 60 * 5
    encode.update({"exp": expires})
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def create_refresh_token(created_user: Users):
    encode = {
        "username": created_user.username,
        "id": created_user.id,
        "role": created_user.role,
    }
    expires = int(time()) + 60 * 60 * 24
    encode.update({"exp": expires})
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


async def verify_token(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)]
):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        now = int(time())
        if payload.get("exp") < now:
            raise HTTPException(status_code=401, detail="Token Expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token or token expired")
    return token


def read_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
