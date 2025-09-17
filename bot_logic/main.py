from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher
from bot_logic.bot_services.bot_functions.bot_instanse import bot
from bot_logic.handlers.start_handle import router
from bot_logic.handlers.add_channel_handler import adding_router
from bot_logic.handlers.channel_settings_handler import setting_router
from bot_logic.handlers.time_handler import time_router
from bot_logic.bot_services.database.models import create_tables


async def main():
    create_tables()
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(router, adding_router, setting_router, time_router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
