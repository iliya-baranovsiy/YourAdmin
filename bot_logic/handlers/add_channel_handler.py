from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot_logic.bot_services.keybords.keybords import *
from bot_logic.bot_services.bot_functions.help_functions import check_channel
from bot_logic.bot_services.bot_functions.states import WaitChannelId
from bot_logic.bot_services.keybords.adding_kb import *

adding_router = Router()


@adding_router.callback_query(F.data == 'add_channel')
async def add_channel(call: CallbackQuery, state: FSMContext):
    buttons = InlineKeyboardMarkup(inline_keyboard=back_to_menu)
    await call.message.answer('Введи id канала, который хочешь добавить', reply_markup=buttons)
    await state.set_state(WaitChannelId.wait_id)


@adding_router.message(F.text, WaitChannelId.wait_id)
async def get_id(msg: Message, state: FSMContext):
    channel_id = msg.text
    status = await check_channel(int(channel_id))
    if status:
        buttons = InlineKeyboardMarkup(inline_keyboard=settings_or_menu)
        await msg.answer('Канал привязан', reply_markup=buttons)
        await state.clear()
    else:
        buttons = InlineKeyboardMarkup(inline_keyboard=back_to_menu)
        await msg.answer('Ошибка при привязке попробуй ещё раз или вернись в меню', reply_markup=buttons)


