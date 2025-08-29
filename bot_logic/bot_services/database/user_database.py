from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import insert
from configurations.loadEnv import ASYNC_DATA_BASE_URL
from sqlalchemy import select
from bot_logic.bot_services.database.models import User, Channels

Base = declarative_base()


class UserDbWork:
    def __init__(self):
        self.__async_engine = create_async_engine(url=ASYNC_DATA_BASE_URL)
        self.session = async_sessionmaker(self.__async_engine, expire_on_commit=False)

    async def write_user(self, tg_id, count=None):
        async with self.session() as session:
            async with session.begin():
                new_user = insert(User).values(tg_id=tg_id, channel_count=count)
                new_user = new_user.on_conflict_do_nothing(index_elements=['tg_id'])
                await session.execute(new_user)


class ChannelWork:
    def __init__(self):
        self.__async_engine = create_async_engine(url=ASYNC_DATA_BASE_URL)
        self.session = async_sessionmaker(self.__async_engine, expire_on_commit=False)

    async def get_user_channels(self, owner_id):
        async with self.session() as session:
            async with session.begin():
                channels_id = select(Channels.channel_id).where(Channels.owner == owner_id)
                result = await session.execute(channels_id)
                channels_id = result.scalars().all()
                return channels_id


users_db = UserDbWork()
channels_db_work = ChannelWork()
#print(asyncio.run(channels_db_work.get_user_channels(1)))
