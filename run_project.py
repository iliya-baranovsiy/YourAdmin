from scraping.scrap import clean_db, run_scraping
import threading
from bot_logic.main import main
from bot_logic.bot_services.bot_functions.time_tracker import track_time
from bot_logic.bot_services.bot_functions.default_by_time import set_default_count_by_time
import asyncio


async def run_async_func():
    task_bot = asyncio.create_task(main())
    task_tracker = asyncio.create_task(track_time())
    task_set_default_count = asyncio.create_task(set_default_count_by_time())
    await asyncio.gather(task_bot, task_tracker, task_set_default_count)


if __name__ == '__main__':
    """clean = threading.Thread(target=clean_db)
    run_scrap = threading.Thread(target=run_scraping)
    run_scrap.start()
    clean.start()"""
    asyncio.run(run_async_func())
