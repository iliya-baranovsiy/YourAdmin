from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import insert
from configurations.loadEnv import ASYNC_DATA_BASE_URL
from sqlalchemy import select, update, delete
from bot_logic.bot_services.database.models import User, Channels, TimesIntervals
import asyncio

Base = declarative_base()


class BaseWork:
    def __init__(self):
        self.__async_engine = create_async_engine(url=ASYNC_DATA_BASE_URL)
        self.session = async_sessionmaker(self.__async_engine, expire_on_commit=False)


class UserDbWork(BaseWork):

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


class ChannelWork(BaseWork):

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

    async def plus_posts_a_day(self, channel_id):
        async with self.session() as session:
            async with session.begin():
                new = update(Channels).where(Channels.channel_id == channel_id).values(
                    post_count=Channels.post_count + 1)
                await session.execute(new)


class TimesIntervalsWork(BaseWork):
    async def set_time(self, channel_id, target_time):
        async with self.session() as session:
            async with session.begin():
                new_time = insert(TimesIntervals).values(channel_id=int(channel_id), time=target_time)
                await session.execute(new_time)

    async def delete_time(self, channel_id, time_to_del):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(
                    select(TimesIntervals).where(
                        TimesIntervals.channel_id == int(channel_id),
                        TimesIntervals.time == time_to_del
                    )
                )
                row = result.scalar_one_or_none()
                await session.delete(row)

    async def get_times(self, channel_id):
        async with self.session() as session:
            async with session.begin():
                query = select(TimesIntervals.time).where(TimesIntervals.channel_id == int(channel_id))
                result = await session.execute(query)
                rows = result.all()
                return rows


users_db = UserDbWork()
channels_db_work = ChannelWork()
times_db = TimesIntervalsWork()
# print(asyncio.run(channels_db_work.get_date_count(-1002798314681)))
# asyncio.run(channels_db_work.get_channel_settings(-1002798314681))
# print(asyncio.run(channels_db_work.get_user_channels(1832511762)))
