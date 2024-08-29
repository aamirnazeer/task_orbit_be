from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, UUID
from time import time
import uuid


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    uuid = Column(UUID, default=uuid.uuid4)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    role = Column(String)
    phone_number = Column(String)
    is_active = Column(Boolean, nullable=False, default=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_on = Column(Integer, nullable=False, default=int(time()))
    last_updated_on = Column(Integer, nullable=False, default=int(time()), onupdate=int(time()))