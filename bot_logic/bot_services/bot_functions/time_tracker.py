import asyncio
import time
from bot_logic.bot_services.bot_functions.sender import send_post
from bot_logic.bot_services.database.user_database import send_logic_db
from datetime import datetime, timedelta


async def track_time():
    now = datetime.now()
    next_minute = (now.replace(second=0, microsecond=0) + timedelta(minutes=1))
    wait_seconds = (next_minute - now).total_seconds()
    await asyncio.sleep(wait_seconds)
    while True:
        now_str = datetime.now().time().strftime("%H:%M")
        channel_ids = await send_logic_db.get_channels_with_target_time(now_str)
        if channel_ids:
            tasks = [send_post(id_) for id_ in channel_ids]
            await asyncio.gather(*tasks)
        await asyncio.sleep(60)
