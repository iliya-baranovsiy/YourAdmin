from .bot_instanse import bot
from bot_logic.bot_services.database.user_database import channels_db_work, send_logic_db


async def send_post(channel_id):
    post_count = await channels_db_work.get_post_count(channel_id)
    settings = await channels_db_work.get_channel_settings(channel_id=channel_id)
    owner_id = await channels_db_work.get_channel_owner_id(channel_id)
    theme = settings[0]
    if post_count < 3:
        news = await send_logic_db.get_news(channel_id=channel_id, news_theme=theme)
        news_title = news[1]
        text = news[0]
        picture = news[2]
        try:
            await bot.send_photo(chat_id=channel_id, photo=picture, caption=text, parse_mode="HTML")
            await channels_db_work.plus_posts_a_day(channel_id=channel_id)
            await send_logic_db.add_publish(channel_id=channel_id, news_title=news_title)
            await bot.send_message(chat_id=owner_id, text="ОТправлено")
        except:
            try:
                await bot.send_message(chat_id=channel_id, text=text, parse_mode="HTML")
                await channels_db_work.plus_posts_a_day(channel_id=channel_id)
                await send_logic_db.add_publish(channel_id=channel_id, news_title=news_title)
                await bot.send_message(chat_id=owner_id, text="ОТправлено")
            except:
                await bot.send_message(chat_id=owner_id, text="Ошибка при отправке")
    else:
        await bot.send_message(chat_id=owner_id, text="Суточное кол-во постов превышено")
