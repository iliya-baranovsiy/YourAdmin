from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from bot_logic.bot_services.user_database import users_db
import asyncio
from bot_logic.bot_services.keybords import *

router = Router()


@router.message(CommandStart())
async def start_dialog(msg: Message):
    tg_id = msg.chat.id
    buttons = InlineKeyboardMarkup(inline_keyboard=main_menu)
    await msg.answer('Привет, здесь будет приветствие и краткая информация, ещё причешим :)')
    await users_db.write_user(tg_id=tg_id)
    await asyncio.sleep(2)
    await msg.answer('Главное меню 📊', reply_markup=buttons)


@router.callback_query(F.data == "my_channels")
async def user_channels(call: CallbackQuery):
    await call.message.edit_text("Твои каналы")


@router.callback_query(F.data == "service_info")
async def information(call: CallbackQuery):
    await call.message.edit_text("Информация")


@router.callback_query(F.data == "how_add_channel")
async def how_add(call: CallbackQuery):
    await call.message.edit_text("Инструкция")
