from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import insert
from configurations.loadEnv import ASYNC_DATA_BASE_URL
from sqlalchemy import select, update, delete
from bot_logic.bot_services.database.models import User, Channels
import asyncio

Base = declarative_base()


class UserDbWork:
    def __init__(self):
        self.__async_engine = create_async_engine(url=ASYNC_DATA_BASE_URL)
        self.session = async_sessionmaker(self.__async_engine, expire_on_commit=False)

    async def write_user(self, tg_id):
        async with self.session() as session:
            async with session.begin():
                new_user = insert(User).values(tg_id=tg_id)
                new_user = new_user.on_conflict_do_nothing(index_elements=['tg_id'])
                await session.execute(new_user)

    async def get_channel_count(self, tg_id):
        async with self.session() as session:
            async with session.begin():
                count = select(User.channel_count).where(User.tg_id == tg_id)
                result = await session.execute(count)
                return result.scalar()

    async def update_channel_count(self, tg_id, operate):
        async with self.session() as session:
            async with session.begin():
                if operate == '+':
                    new = update(User).where(User.tg_id == tg_id).values(channel_count=User.channel_count + 1)
                else:
                    new = update(User).where(User.tg_id == tg_id).values(channel_count=User.channel_count - 1)
                await session.execute(new)


class ChannelWork:
    def __init__(self):
        self.__async_engine = create_async_engine(url=ASYNC_DATA_BASE_URL)
        self.session = async_sessionmaker(self.__async_engine, expire_on_commit=False)

    async def get_user_channels(self, owner_id):
        async with self.session() as session:
            async with session.begin():
                query = select(Channels.channel_id, Channels.title).where(Channels.owner == owner_id)
                result = await session.execute(query)
                rows = result.all()
                data_dict = {title: channel_id for channel_id, title in rows}
                return data_dict

    async def write_channel(self, channel_id, owner, title):
        async with self.session() as session:
            async with session.begin():
                new_channel = insert(Channels).values(channel_id=channel_id, owner=owner, title=title)
                await session.execute(new_channel)

    async def delete_channel(self, channel_id):
        async with self.session() as session:
            async with session.begin():
                channel_to_delete = await session.get(Channels, int(channel_id))
                await session.delete(channel_to_delete)

    async def set_theme(self, channel_id, theme):
        async with self.session() as session:
            async with session.begin():
                if theme == 'sport':
                    new = update(Channels).where(Channels.channel_id == channel_id).values(
                        theme=theme)
                elif theme == 'crypto':
                    new = update(Channels).where(Channels.channel_id == channel_id).values(
                        theme=theme)
                elif theme == 'game':
                    new = update(Channels).where(Channels.channel_id == channel_id).values(
                        theme=theme)
                elif theme == 'it':
                    new = update(Channels).where(Channels.channel_id == channel_id).values(
                        theme=theme)
                elif theme == 'culture':
                    new = update(Channels).where(Channels.channel_id == channel_id).values(
                        theme=theme)
                elif theme == 'science':
                    new = update(Channels).where(Channels.channel_id == channel_id).values(
                        theme=theme)
                await session.execute(new)

    async def set_post_type(self, channel_id, post_type):
        async with self.session() as session:
            async with session.begin():
                if post_type == 'news':
                    new = update(Channels).where(Channels.channel_id == channel_id).values(
                        type=post_type)
                await session.execute(new)

    async def get_channel_settings(self, channel_id):
        async with self.session() as session:
            async with session.begin():
                query = select(Channels.theme, Channels.type).where(Channels.channel_id == channel_id)
                result = await session.execute(query)
                rows = result.all()
                return rows[0]


users_db = UserDbWork()
channels_db_work = ChannelWork()
#asyncio.run(channels_db_work.get_channel_settings(-1002798314681))
# print(asyncio.run(channels_db_work.get_user_channels(1832511762)))
