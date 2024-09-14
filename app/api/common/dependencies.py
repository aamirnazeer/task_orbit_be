from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.api.common.utils import verify_token
from app.core.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
token_dependency = Annotated[HTTPAuthorizationCredentials, Depends(verify_token)]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
