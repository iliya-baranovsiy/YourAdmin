from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, create_engine, String, DateTime, BigInteger, ForeignKey
from configurations.loadEnv import DATA_BASE_URL
import asyncio

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    tg_id = Column(BigInteger, primary_key=True)
    channel_count = Column(Integer, default=0)


class Channels(Base):
    __tablename__ = 'channels'
    channel_id = Column(BigInteger, primary_key=True)
    owner = Column(Integer)
    title = Column(String)
    theme = Column(String, default=None)
    type = Column(String, default=None)

    times = relationship("TimesIntervals", back_populates="channel", cascade="all, delete, delete-orphan")
    published = relationship("PublishNews", back_populates='channel', cascade='all, delete, delete-orphan')


class TimesIntervals(Base):
    __tablename__ = 'times_intervals'
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(BigInteger, ForeignKey('channels.channel_id', ondelete='CASCADE'))
    time = Column(String)

    channel = relationship("Channels", back_populates="times")


class PublishNews(Base):
    __tablename__ = "publish_news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(BigInteger, ForeignKey('channels.channel_id', ondelete='CASCADE'))
    news_title = Column(String)

    channel = relationship("Channels", back_populates="published")


class ChannelsPosts(Base):
    __tablename__ = "channel_posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(BigInteger)
    post_count = Column(Integer, default=0)


def create_tables():
    engine = create_engine(DATA_BASE_URL)
    Base.metadata.create_all(engine)

create_tables()
