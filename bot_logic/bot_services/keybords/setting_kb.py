from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


async def channel_info_kb(channel_id, channel_name):
    channel_info_menu = [
        [InlineKeyboardButton(text="Настройки постинга", callback_data=f'settings_{channel_id}_{channel_name}')],
        [InlineKeyboardButton(text="Удалить канал", callback_data=f'delete_{channel_id}_{channel_name}')],
        [InlineKeyboardButton(text='Вернуться в назад ⬅️', callback_data='back_to_chan_info')]
    ]
    return channel_info_menu


async def agree_or_not(channel_id, channel_name):
    agree_with_delete = [
        [InlineKeyboardButton(text="Да", callback_data=f'agree_{channel_id}'),
         InlineKeyboardButton(text="Нет", callback_data=f'backtochanmenu_{channel_id}_{channel_name}')]
    ]
    return agree_with_delete


back_to_main = [
    [InlineKeyboardButton(text='Вернуться в меню 📊', callback_data='back_main_menu')]
]
