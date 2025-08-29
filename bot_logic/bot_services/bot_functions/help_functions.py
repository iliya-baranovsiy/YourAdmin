from bot_logic.bot_services.bot_functions.bot_instanse import bot
import asyncio


async def check_channel(channel_id):
    try:
        chat = await bot.get_chat(chat_id=int(channel_id))
        if chat.type in ['channel']:
            return '@' + chat.username
        else:
            return None
    except:
        return None


async def refactoring(text):
    if text == 'sport':
        return 'спорт'
    elif text == 'culture':
        return 'культура'
    elif text == 'crypto':
        return 'крипта'
    elif text == 'it':
        return 'IT/технологии'
    elif text == 'science':
        return 'наука'
    elif text == 'game':
        return 'игры'
    elif text == 'news':
        return 'новости'

# print(asyncio.run(is_admin_in_channel(-1002989249599)))
