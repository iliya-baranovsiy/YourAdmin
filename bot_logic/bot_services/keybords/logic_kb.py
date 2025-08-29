from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bot_logic.bot_services.database.user_database import channels_db_work


async def chanells_kb(owner_id, count_channels):
    result_buttons = []
    work_dict = await channels_db_work.get_user_channels(owner_id=owner_id)
    for key, value in work_dict.items():
        result_buttons.append([InlineKeyboardButton(text=key, callback_data=f'channel_{value}_{key}')])
    if count_channels < 2:
        result_buttons.append([InlineKeyboardButton(text='Добавить канал 🚀', callback_data='add_channel')])
    result_buttons.append([InlineKeyboardButton(text='Вернуться в меню 📊', callback_data='back_main_menu')])
    return result_buttons
