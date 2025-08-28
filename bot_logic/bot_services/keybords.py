from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

main_menu = [
    [InlineKeyboardButton(text='Мои каналы 🎯', callback_data='my_channels')],
    [InlineKeyboardButton(text='Информация о сервисе 📝', callback_data='service_info')],
    [InlineKeyboardButton(text='Как добавить кнаал ❓', callback_data='how_add_channel')]
]
