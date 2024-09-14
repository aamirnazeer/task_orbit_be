from time import time

from app.core.database import Base
from sqlalchemy import Column, Integer, String


class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String)
    created_on = Column(Integer, nullable=False, default=int(time()))
