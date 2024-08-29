from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core import env

engine = create_engine(env.SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

