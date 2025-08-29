from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from bot_logic.bot_services.database.user_database import users_db, channels_db_work
import asyncio
from bot_logic.bot_services.keybords.keybords import *
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

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
    tg_id = call.message.chat.id
    user_channels = await channels_db_work.get_user_channels(owner_id=tg_id)
    if not user_channels:
        buttons = InlineKeyboardMarkup(inline_keyboard=add_channel_menu)
        await call.message.edit_text("Список твоих каналов пуст. Ты моежшь добавить новый канал 👇",
                                     reply_markup=buttons)
    else:
        pass


@router.callback_query(F.data == "service_info")
async def information(call: CallbackQuery):
    await call.message.edit_text("Информация")


@router.callback_query(F.data == "how_add_channel")
async def how_add(call: CallbackQuery):
    await call.message.edit_text("Инструкция")


@router.callback_query(F.data == "back_main_menu")
async def back_main_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    buttons = InlineKeyboardMarkup(inline_keyboard=main_menu)
    await call.message.edit_text('Главное меню 📊', reply_markup=buttons)


@router.message(StateFilter(None))
async def free_mes(msg: Message):
    buttons = InlineKeyboardMarkup(inline_keyboard=main_menu)
    await msg.answer('Выбери один пункт из меню, чтобы продолжить ☺️', reply_markup=buttons)
