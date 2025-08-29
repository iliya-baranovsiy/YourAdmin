from bot_logic.bot_services.bot_functions.bot_instanse import bot


async def check_channel(channel_id):
    try:
        chat = await bot.get_chat(chat_id=channel_id)
        if chat.type in ['channel', 'supergroup']:
            return '@' + chat.username
        else:
            return None
    except:
        return None

# print(asyncio.run(check_channel(-1002989249599)))
#
