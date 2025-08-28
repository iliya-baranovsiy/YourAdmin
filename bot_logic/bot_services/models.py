from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, create_engine
from configurations.loadEnv import DATA_BASE_URL
import asyncio

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    tg_id = Column(Integer, primary_key=True)
    channel_count = Column(Integer, default=0)


def create_tables():
    engine = create_engine(DATA_BASE_URL)
    Base.metadata.create_all(engine)


create_tables()
