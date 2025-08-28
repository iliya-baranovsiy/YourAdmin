from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher
import asyncio
from bot_services.bot_instanse import bot
from handlers.start_handle import router


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
