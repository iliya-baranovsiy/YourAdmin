from .bot_instanse import bot
from bot_logic.bot_services.database.user_database import channels_db_work, send_logic_db
from bot_logic.bot_services.keybords.adding_kb import *


async def send_post(channel_id):
    post_count = await channels_db_work.get_post_count(channel_id)
    settings = await channels_db_work.get_channel_settings(channel_id=channel_id)
    owner_id = await channels_db_work.get_channel_owner_id(channel_id)
    theme = settings[0]
    buttons = InlineKeyboardMarkup(inline_keyboard=back_to_menu)
    if post_count < 3:
        news = await send_logic_db.get_news(channel_id=channel_id, news_theme=theme)
        news_title = news[1]
        text = news[0]
        picture = news[2]
        try:
            await bot.send_photo(chat_id=channel_id, photo=picture, caption=text, parse_mode="HTML")
            await channels_db_work.plus_posts_a_day(channel_id=channel_id)
            await send_logic_db.add_publish(channel_id=channel_id, news_title=news_title)
        except:
            try:
                await bot.send_message(chat_id=channel_id, text=text, parse_mode="HTML")
                await channels_db_work.plus_posts_a_day(channel_id=channel_id)
                await send_logic_db.add_publish(channel_id=channel_id, news_title=news_title)
            except:
                await bot.send_message(chat_id=owner_id,
                                       text="Ошибка при отправке поста, проверь настройки канла или обратись в поддержку 😊",
                                       reply_markup=buttons)
    else:
        await bot.send_message(chat_id=owner_id, text="Пост не отправлен. Суточное кол-во постов превышено 🤯",
                               reply_markup=buttons)
