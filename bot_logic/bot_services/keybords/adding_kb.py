from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

back_to_menu = [
    [InlineKeyboardButton(text='Вернуться в меню 📊', callback_data='back_main_menu')]
]


async def settings_or_menu(channel_id, channel_name):
    buttons = [
        [InlineKeyboardButton(text='Настроить постинг в канале ⚙️',
                              callback_data=f'settings_{channel_id}_{channel_name}')],
        [InlineKeyboardButton(text='Вернуться в меню 📊', callback_data='back_main_menu')]
    ]
    return buttons
