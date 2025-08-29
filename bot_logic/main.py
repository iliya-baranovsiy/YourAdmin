from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher
import asyncio
from bot_logic.bot_services.bot_functions.bot_instanse import bot
from handlers.start_handle import router
from handlers.add_channel_handler import adding_router
from handlers.channel_settings_handler import setting_router


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(router, adding_router,setting_router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
