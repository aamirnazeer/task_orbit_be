import os
from typing import Annotated

import pytest
from alembic import command
from alembic.config import Config
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.testclient import TestClient
from sqlalchemy import create_engine


from app.api.common.dependencies import get_db
from app.api.common.utils import verify_token
from app.main import app
from sqlalchemy.orm import sessionmaker


engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URL_TEST"))
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)
security = HTTPBearer()


def test_db_dependency():
    db = SessionTesting()
    try:
        command.upgrade(Config("alembic.ini"), "head")
        yield db
    finally:
        db.close()


def mock_verify_token(token: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    if not token.credentials == 'mocked_token':
        raise HTTPException(status_code=401, detail='Invalid token')
    return token


app.dependency_overrides[get_db] = test_db_dependency
app.dependency_overrides[verify_token] = mock_verify_token


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


def pytest_configure():
    os.environ["ENV"] = 'test'


def pytest_unconfigure():
    command.downgrade(Config("alembic.ini"), "base")

