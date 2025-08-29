from aiogram import F, Router
from aiogram.types import Message
from bot_logic.bot_services.database.user_database import users_db, channels_db_work
from bot_logic.bot_services.keybords.setting_kb import *

setting_router = Router()


@setting_router.callback_query(F.data.startswith(("channel")))
async def channel_menu(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    buttons = InlineKeyboardMarkup(inline_keyboard=await channel_info_kb(channel_id, channel_name))
    await call.message.edit_text(f'Меню по каналу {channel_name}', reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("delete")))
async def question(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    buttons = InlineKeyboardMarkup(inline_keyboard=await agree_or_not(channel_id, channel_name))
    await call.message.edit_text(f"Ты уверен, что хочешь удалить {channel_name} из списка каналов ?",
                                 reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("agree")))
async def agree_with_delete(call: CallbackQuery):
    channel_id = call.data.split('_')[1]
    owner_id = call.message.chat.id
    buttons = InlineKeyboardMarkup(inline_keyboard=back_to_main)
    try:
        await channels_db_work.delete_channel(channel_id)
        await users_db.update_channel_count(tg_id=owner_id, operate='-')
        await call.message.edit_text("Канал удален успешно", reply_markup=buttons)
    except:
        await call.message.edit_text("Ошибка при удалении", reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("backtochanmenu")))
async def back_to_channel_menu(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    buttons = InlineKeyboardMarkup(inline_keyboard=await channel_info_kb(channel_id, channel_name))
    await call.message.edit_text(f'Меню по каналу {channel_name}', reply_markup=buttons)
