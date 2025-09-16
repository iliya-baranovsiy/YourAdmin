from bot_logic.bot_services.database.user_database import channels_db_work
from datetime import datetime, timedelta
import asyncio


async def set_default_count_by_time():
    while True:
        now = datetime.now().hour
        if now == 1:
            await channels_db_work.set_default_post_count()
        await asyncio.sleep(86400)
