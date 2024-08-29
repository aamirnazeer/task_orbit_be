from time import time

from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, UUID, ForeignKey
import uuid


class Cards(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    uuid = Column(UUID, default=uuid.uuid4)
    title = Column(String)