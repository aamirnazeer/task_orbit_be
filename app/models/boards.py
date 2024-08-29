from time import time

from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, UUID, ForeignKey
import uuid


class Boards(Base):
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    uuid = Column(UUID, default=uuid.uuid4)
    board_name = Column(String)
    board_owner = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, nullable=False, default=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_on = Column(Integer, nullable=False, default=int(time()))
    last_updated_on = Column(Integer, nullable=False, default=int(time()), onupdate=int(time()))
