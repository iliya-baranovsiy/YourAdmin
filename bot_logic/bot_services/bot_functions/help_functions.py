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

# print(asyncio.run(is_admin_in_channel(-1002989249599)))
