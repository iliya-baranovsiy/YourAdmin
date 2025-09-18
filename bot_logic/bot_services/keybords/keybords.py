from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

main_menu = [
    [InlineKeyboardButton(text='Мои каналы 🎯', callback_data='my_channels')],
    [InlineKeyboardButton(text='Информация о сервисе 📝', callback_data='service_info')],
    [InlineKeyboardButton(text='Как добавть канал ❓',callback_data='how_add_channel')],
    [InlineKeyboardButton(text='Узнать ID канала 🔑', callback_data='know_channel_id')]
]

add_channel_menu = [
    [InlineKeyboardButton(text='Добавить канал 🚀', callback_data='add_channel')],
    [InlineKeyboardButton(text='Вернуться в меню 📊', callback_data='back_main_menu')]
]
