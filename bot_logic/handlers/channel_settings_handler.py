from aiogram import F, Router
from aiogram.types import Message
from bot_logic.bot_services.database.user_database import users_db, channels_db_work
from bot_logic.bot_services.keybords.setting_kb import *
from bot_logic.bot_services.bot_functions.help_functions import refactoring
from bot_logic.bot_services.bot_functions.sender import send_post

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

    await call.message.edit_text(
        f"Меню по каналу {channel_name}", reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("settings")))
async def setting_menu(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    data_choice = await channels_db_work.get_channel_settings(channel_id=int(channel_id))
    topic_theme = f"Тема: {await refactoring(data_choice[0]) if data_choice[0] is not None else 'Не указана'}\n"
    topic_type = f"Тип поста: {await refactoring(data_choice[1]) if data_choice[1] is not None else 'Не указана'}"
    topic_text = topic_theme + topic_type
    buttons = InlineKeyboardMarkup(inline_keyboard=await posting_menu(channel_id=channel_id, channel_name=channel_name))
    await call.message.edit_text(f"Настройки постинга для {channel_name}\n{topic_text}", reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("theme")))
async def theme_menu_f(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    buttons = InlineKeyboardMarkup(inline_keyboard=await theme_menu(channel_id, channel_name))
    await call.message.edit_text("Выбери тему для постов", reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("postnigmenu")))
async def back_to_posting_settings(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    data_choice = await channels_db_work.get_channel_settings(channel_id=int(channel_id))
    topic_theme = f"Тема: {await refactoring(data_choice[0]) if data_choice[0] is not None else 'Не указана'}\n"
    topic_type = f"Тип поста: {await refactoring(data_choice[1]) if data_choice[1] is not None else 'Не указана'}"
    topic_text = topic_theme + topic_type
    buttons = InlineKeyboardMarkup(inline_keyboard=await posting_menu(channel_id=channel_id, channel_name=channel_name))
    await call.message.edit_text(f"Настройки постинга для {channel_name}\n{topic_text}", reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("game")))
async def set_game_theme(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    try:
        await channels_db_work.set_theme(channel_id=int(channel_id), theme='game')
        buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_settings_menu(channel_id, channel_name))
        await call.message.edit_text('Тема установлена успешно, чтобы сменить тему, просто выбери другую',
                                     reply_markup=buttons)
    except:
        buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_settings_menu(channel_id, channel_name))
        await call.message.edit_text('Произошла ошика, поробуй ещё раз',
                                     reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("it")))
async def set_it_theme(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    try:
        await channels_db_work.set_theme(channel_id=int(channel_id), theme='it')
        buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_settings_menu(channel_id, channel_name))
        await call.message.edit_text('Тема установлена успешно, чтобы сменить тему, просто выбери другую',
                                     reply_markup=buttons)
    except:
        buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_settings_menu(channel_id, channel_name))
        await call.message.edit_text('Произошла ошика, поробуй ещё раз',
                                     reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("crypto")))
async def set_crypto_theme(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    try:
        await channels_db_work.set_theme(channel_id=int(channel_id), theme='crypto')
        buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_settings_menu(channel_id, channel_name))
        await call.message.edit_text('Тема установлена успешно, чтобы сменить тему, просто выбери другую',
                                     reply_markup=buttons)
    except:
        buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_settings_menu(channel_id, channel_name))
        await call.message.edit_text('Произошла ошика, поробуй ещё раз',
                                     reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("sport")))
async def set_sport_theme(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    try:
        await channels_db_work.set_theme(channel_id=int(channel_id), theme='sport')
        buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_settings_menu(channel_id, channel_name))
        await call.message.edit_text('Тема установлена успешно, чтобы сменить тему, просто выбери другую',
                                     reply_markup=buttons)
    except:
        buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_settings_menu(channel_id, channel_name))
        await call.message.edit_text('Произошла ошика, поробуй ещё раз',
                                     reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("culture")))
async def set_culture_theme(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    try:
        await channels_db_work.set_theme(channel_id=int(channel_id), theme='culture')
        buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_settings_menu(channel_id, channel_name))
        await call.message.edit_text('Тема установлена успешно, чтобы сменить тему, просто выбери другую',
                                     reply_markup=buttons)
    except:
        buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_settings_menu(channel_id, channel_name))
        await call.message.edit_text('Произошла ошика, поробуй ещё раз',
                                     reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("science")))
async def set_science_theme(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    try:
        await channels_db_work.set_theme(channel_id=int(channel_id), theme='science')
        buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_settings_menu(channel_id, channel_name))
        await call.message.edit_text('Тема установлена успешно, чтобы сменить тему, просто выбери другую',
                                     reply_markup=buttons)
    except:
        buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_settings_menu(channel_id, channel_name))
        await call.message.edit_text('Произошла ошика, поробуй ещё раз',
                                     reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("type")))
async def type_menu_handler(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    buttons = InlineKeyboardMarkup(inline_keyboard=await type_menu(channel_id, channel_name))
    await call.message.edit_text('Выбери тип новости',
                                 reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("news")))
async def set_news_type(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    try:
        await channels_db_work.set_post_type(channel_id=int(channel_id), post_type='news')
        buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_settings_menu(channel_id, channel_name))
        await call.message.edit_text('Тип установлена успешно, чтобы сменить тип, просто выбери другую',
                                     reply_markup=buttons)
    except:
        buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_settings_menu(channel_id, channel_name))
        await call.message.edit_text('Произошла ошика, поробуй ещё раз',
                                     reply_markup=buttons)


@setting_router.callback_query(F.data.startswith(("makepost")))
async def make_post(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    await send_post(int(channel_id))
    buttons = InlineKeyboardMarkup(inline_keyboard=await channel_info_kb(channel_id, channel_name))

    await call.message.answer(
        f"Меню по каналу {channel_name}", reply_markup=buttons)
