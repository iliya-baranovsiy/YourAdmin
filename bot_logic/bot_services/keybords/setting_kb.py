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


async def posting_menu(channel_id, channel_name):
    buttons = [
        [InlineKeyboardButton(text='Выбрать тему постов', callback_data=f'theme_{channel_id}_{channel_name}')],
        [InlineKeyboardButton(text='Выбрать тип постов', callback_data=f'type_{channel_id}_{channel_name}')],
        [InlineKeyboardButton(text='Время постов', callback_data=f'time_{channel_id}_{channel_name}')],
        [InlineKeyboardButton(text='Вернуться в меню 📊', callback_data='back_main_menu')]
    ]
    return buttons


async def theme_menu(channel_id, channel_name):
    buttons = [
        [
            InlineKeyboardButton(text='Игры', callback_data=f'game_{channel_id}_{channel_name}'),
            InlineKeyboardButton(text='IT/технологии', callback_data=f'it_{channel_id}_{channel_name}')
        ],
        [
            InlineKeyboardButton(text='Криптовалюта', callback_data=f'crypto_{channel_id}_{channel_name}'),
            InlineKeyboardButton(text='Спорт', callback_data=f'sport_{channel_id}_{channel_name}')
        ],
        [
            InlineKeyboardButton(text='Культура', callback_data=f'culture_{channel_id}_{channel_name}'),
            InlineKeyboardButton(text='Наука', callback_data=f'science_{channel_id}_{channel_name}')
        ],
        [InlineKeyboardButton(text="Вернуться назад", callback_data=f'postnigmenu_{channel_id}_{channel_name}')]
    ]
    return buttons


async def back_to_settings_menu(channel_id, channel_name):
    buttons = [
        [InlineKeyboardButton(text="Вернуться назад", callback_data=f'postnigmenu_{channel_id}_{channel_name}')]
    ]
    return buttons


async def type_menu(channel_id, channel_name):
    buttons = [
        [InlineKeyboardButton(text='Новости', callback_data=f'news_{channel_id}_{channel_name}')],
        [InlineKeyboardButton(text="Вернуться назад", callback_data=f'postnigmenu_{channel_id}_{channel_name}')]
    ]
    return buttons
