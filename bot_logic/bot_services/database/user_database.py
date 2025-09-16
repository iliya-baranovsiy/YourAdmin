from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import insert
from configurations.loadEnv import ASYNC_DATA_BASE_URL
from sqlalchemy import select, update, delete, func
from bot_logic.bot_services.database.models import User, Channels, TimesIntervals, PublishNews, ChannelsPosts
from services.scrap_db_work import ItNews, CultureNews, CryptoNews, SportNews, ScienceNews, GameNews
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

    async def get_channels_from_post(self):
        async with self.session() as session:
            async with session.begin():
                query = select(ChannelsPosts.channel_id)
                result = await session.execute(query)
                res_list = [i[0] for i in result.all()]
                return res_list

    async def write_channel(self, channel_id, owner, title):
        async with self.session() as session:
            async with session.begin():
                new_channel = insert(Channels).values(channel_id=channel_id, owner=owner, title=title)
                await session.execute(new_channel)
                channels = await self.get_channels_from_post()
                if channel_id in channels:
                    pass
                else:
                    new_channel_in_counts = insert(ChannelsPosts).values(channel_id=channel_id)
                    await session.execute(new_channel_in_counts)

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
                new = update(ChannelsPosts).where(ChannelsPosts.channel_id == channel_id).values(
                    post_count=ChannelsPosts.post_count + 1)
                await session.execute(new)

    async def get_post_count(self, channel_id):
        async with self.session() as session:
            async with session.begin():
                query = select(ChannelsPosts.post_count).where(ChannelsPosts.channel_id == channel_id)
                result = await session.execute(query)
                rows = result.scalar_one_or_none()
                return rows

    async def get_channel_owner_id(self, channel_id):
        async with self.session() as session:
            async with session.begin():
                query = select(Channels.owner).where(Channels.channel_id == int(channel_id))
                result = await session.execute(query)
                owner_id = result.scalar()
                return owner_id

    async def set_default_post_count(self):
        async with self.session() as session:
            async with session.begin():
                new = update(ChannelsPosts).values(
                    post_count=0)
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
                rows = [i[0] for i in result.all()]
                return rows


class SendLogic(BaseWork):
    async def add_publish(self, channel_id, news_title):
        async with self.session() as session:
            async with session.begin():
                new_publish = insert(PublishNews).values(channel_id=channel_id, news_title=news_title)
                await session.execute(new_publish)

    async def get_news(self, channel_id, news_theme):
        async with self.session() as session:
            async with session.begin():
                target_table = None
                if news_theme == 'sport':
                    target_table = SportNews
                elif news_theme == 'crypto':
                    target_table = CryptoNews
                elif news_theme == 'game':
                    target_table = GameNews
                elif news_theme == 'it':
                    target_table = ItNews
                elif news_theme == 'culture':
                    target_table = CultureNews
                elif news_theme == 'science':
                    target_table = ScienceNews

                published_subquery = (
                    select(PublishNews.news_title)
                    .where(PublishNews.channel_id == int(channel_id))
                )
                query = (
                    select(target_table.text, target_table.title, target_table.picture)
                    .where(~target_table.title.in_(published_subquery))
                    .order_by(func.random())
                    .limit(1)
                )
                result = await session.execute(query)
                news = result.first()
                return news

    async def get_channels_with_target_time(self, current_time):
        async with self.session() as session:
            async with session.begin():
                query = select(TimesIntervals.channel_id).where(TimesIntervals.time == str(current_time))
                result = await session.execute(query)
                rows = [i[0] for i in result.all()]
                return rows


users_db = UserDbWork()
channels_db_work = ChannelWork()
times_db = TimesIntervalsWork()
send_logic_db = SendLogic()
# print(asyncio.run(channels_db_work.get_post_count(-1002798314681)))
# print(asyncio.run(send_logic_db.get_news(-1002989249599, 'it')))
# print(asyncio.run(channels_db_work.get_date_count(-1002798314681)))
# print(asyncio.run(channels_db_work.get_channel_settings(-1002798314681)))
# print(asyncio.run(channels_db_work.get_user_channels(1832511762)))
# print(asyncio.run(send_logic_db.get_channels_with_target_time('15:30')))
# print(asyncio.run(channels_db_work.get_channel_owner_id(-1002989249599)))
# print(asyncio.run(times_db.get_times(-1002798314681)))
# print(asyncio.run(channels_db_work.set_default_post_count()))
# print(asyncio.run(channels_db_work.get_channels_from_post()))
