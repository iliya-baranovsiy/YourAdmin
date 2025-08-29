from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, create_engine, String, DateTime
from configurations.loadEnv import DATA_BASE_URL
import asyncio

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    tg_id = Column(Integer, primary_key=True)
    channel_count = Column(Integer, default=0)


class Channels(Base):
    __tablename__ = 'channels'
    channel_id = Column(Integer, primary_key=True)
    owner = Column(Integer)
    title = Column(String)
    theme = Column(String, default=None)
    type = Column(String, default=None)
    time = Column(DateTime, default=None)
    post_count = Column(Integer, default=None)


def create_tables():
    engine = create_engine(DATA_BASE_URL)
    Base.metadata.create_all(engine)


create_tables()
