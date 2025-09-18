from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from bot_logic.bot_services.database.user_database import users_db, channels_db_work
import asyncio
from bot_logic.bot_services.keybords.keybords import *
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from bot_logic.bot_services.keybords.logic_kb import chanells_kb
from bot_logic.bot_services.bot_functions.texts import *
from bot_logic.bot_services.bot_functions.states import *
from bot_logic.bot_services.keybords.adding_kb import back_to_menu

router = Router()


@router.message(CommandStart())
async def start_dialog(msg: Message):
    tg_id = msg.chat.id
    buttons = InlineKeyboardMarkup(inline_keyboard=main_menu)
    text = await greetings(msg.chat.first_name)
    await msg.answer(text, parse_mode='HTML')
    await users_db.write_user(tg_id=tg_id)
    await asyncio.sleep(2)
    await msg.answer('Главное меню 📊', reply_markup=buttons)


@router.callback_query(F.data == "my_channels")
async def user_channels(call: CallbackQuery):
    tg_id = call.message.chat.id
    user_channels_count = await users_db.get_channel_count(tg_id=tg_id)
    if user_channels_count == 0:
        buttons = InlineKeyboardMarkup(inline_keyboard=add_channel_menu)
        await call.message.edit_text("Список твоих каналов пуст. Ты моежшь добавить новый канал 👇",
                                     reply_markup=buttons)
    else:
        buttons_list = await chanells_kb(owner_id=tg_id, count_channels=user_channels_count)
        buttons = InlineKeyboardMarkup(inline_keyboard=buttons_list)
        await call.message.edit_text("Твои каналы 👇", reply_markup=buttons)


@router.callback_query(F.data == "service_info")
async def information(call: CallbackQuery):
    buttons = InlineKeyboardMarkup(inline_keyboard=back_to_menu)
    await call.message.edit_text(text=info_text, parse_mode="HTML", reply_markup=buttons)


@router.callback_query(F.data == "how_add_channel")
async def how_add_channel(call: CallbackQuery):
    buttons = InlineKeyboardMarkup(inline_keyboard=back_to_menu)
    await call.message.edit_text(text=how_add_text, parse_mode="HTML", reply_markup=buttons)


@router.callback_query(F.data == "know_channel_id")
async def know_channel_id(call: CallbackQuery, state: FSMContext):
    buttons = InlineKeyboardMarkup(inline_keyboard=back_to_menu)
    await call.message.edit_text("Перешли мне сообщение из канала, ID которого хочешь узнать 😉", reply_markup=buttons)
    await state.set_state(WaitChannelId.wait_forward_message)


@router.message(WaitChannelId.wait_forward_message)
async def get_forward_id(msg: Message, state: FSMContext):
    buttons = InlineKeyboardMarkup(inline_keyboard=back_to_menu)
    if msg.forward_from_chat and msg.forward_from_chat.type == "channel":
        forward_id = str(msg.forward_from_chat.id)
        await msg.answer(f"<b>ID канала:</b> {forward_id}", parse_mode='HTML', reply_markup=buttons)
    else:
        await msg.answer("Я не могу определить откуда это сообщение 😞", reply_markup=buttons)
    await state.clear()


@router.callback_query(F.data == "back_main_menu")
async def back_main_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    buttons = InlineKeyboardMarkup(inline_keyboard=main_menu)
    await call.message.edit_text('Главное меню 📊', reply_markup=buttons)


@router.message(StateFilter(None))
async def free_mes(msg: Message):
    buttons = InlineKeyboardMarkup(inline_keyboard=main_menu)
    if msg.text == '/help':
        await msg.answer("Напиши моему администратору @ilya_baranouski,он всегда поможет ☺️")
        await asyncio.sleep(2)
        await msg.answer('Главное меню 📊', reply_markup=buttons)
    else:
        await msg.answer('Выбери один пункт из меню, чтобы продолжить ☺️', reply_markup=buttons)


@router.callback_query(F.data == 'back_to_chan_info')
async def back_to_channel_menu(call: CallbackQuery):
    tg_id = call.message.chat.id
    user_channels_count = await users_db.get_channel_count(tg_id=tg_id)
    buttons_list = await chanells_kb(owner_id=tg_id, count_channels=user_channels_count)
    buttons = InlineKeyboardMarkup(inline_keyboard=buttons_list)
    await call.message.edit_text("Твои каналы 👇", reply_markup=buttons)
