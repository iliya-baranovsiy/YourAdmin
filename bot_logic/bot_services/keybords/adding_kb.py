from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

back_to_menu = [
    [InlineKeyboardButton(text='Вернуться в меню 📊', callback_data='back_main_menu')]
]

settings_or_menu = [
    [InlineKeyboardButton(text='Настроить постинг в канале ⚙️', callback_data='back_main_menu')],
    [InlineKeyboardButton(text='Вернуться в меню 📊', callback_data='back_main_menu')]
]
