from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


async def manage_time(times: list, channel_id, channel_name):
    buttons = []
    count = len(times)
    if count < 3:
        if times:
            buttons.append(
                [InlineKeyboardButton(text='Добавить время', callback_data=f'addTime_{channel_id}_{channel_name}')])
            for i in times:
                buttons.append(
                    [InlineKeyboardButton(text=f'{i[0]}', callback_data=f'delTime_{i[0]}_{channel_id}_{channel_name}')])
        else:
            buttons.append(
                [InlineKeyboardButton(text='Добавить время', callback_data=f'addTime_{channel_id}_{channel_name}')])
    else:
        for i in times:
            buttons.append(
                [InlineKeyboardButton(text=f'{i[0]}', callback_data=f'delTime_{i[0]}_{channel_id}_{channel_name}')])
    buttons.append(
        [InlineKeyboardButton(text='Вернуться назад', callback_data=f'postnigmenu_{channel_id}_{channel_name}')])
    return buttons


async def back_button(channel_id, channel_name):
    return [[InlineKeyboardButton(text='Назад', callback_data=f'backToTimes_{channel_id}_{channel_name}')]]


async def agree_to_delete_time(channel_id, time_to_delete, channel_name):
    buttons = [
        [InlineKeyboardButton(text='Да',
                              callback_data=f'approveToDelTime_{channel_id}_{time_to_delete}_{channel_name}'),
         InlineKeyboardButton(text='Нет', callback_data=f'backToTimes_{channel_id}_{channel_name}')
         ]
    ]
    return buttons
