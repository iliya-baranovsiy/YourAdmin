from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import insert
from configurations.loadEnv import ASYNC_DATA_BASE_URL
import asyncio
from .models import User

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


users_db = UserDbWork()
