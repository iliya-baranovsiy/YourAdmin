from aiogram import F, Router
from aiogram.types import Message
from bot_logic.bot_services.keybords.time_kb import *
from bot_logic.bot_services.database.user_database import times_db
from aiogram.fsm.context import FSMContext
from bot_logic.bot_services.bot_functions.states import WaitChannelId
from bot_logic.bot_services.bot_functions.help_functions import time_validation
from bot_logic.bot_services.database.user_database import channels_db_work
from datetime import datetime

time_router = Router()


async def show_times_menu(call: CallbackQuery, channel_id, channel_name):
    times = await times_db.get_times(channel_id)
    buttons = InlineKeyboardMarkup(
        inline_keyboard=await manage_time(times=times, channel_id=channel_id, channel_name=channel_name))
    await call.message.edit_text(f"Меню времени канала {channel_name}\nДля удаления времени, нажми на нужное время",
                                 reply_markup=buttons)


@time_router.callback_query(F.data.startswith(("time")))
async def set_times_menu(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    buttons = InlineKeyboardMarkup(inline_keyboard=await back_to_setting_menu(channel_id, channel_name))
    channel_settings = await channels_db_work.get_channel_settings(int(channel_id))
    if channel_settings[0] != None and channel_settings[1] != None:
        await show_times_menu(call, channel_id, channel_name)
    else:
        await call.message.edit_text("Ты не можешь установить время пока не настроишь все пункты постинга",
                                     reply_markup=buttons)


@time_router.callback_query(F.data.startswith(("addTime")))
async def set_time(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    buttons = InlineKeyboardMarkup(inline_keyboard=await back_button(channel_id, channel_name))
    await call.message.edit_text('Напиши время в формате чч:мм', reply_markup=buttons)
    await state.update_data(channel_id=channel_id, channel_name=channel_name)
    await state.set_state(WaitChannelId.wait_input_time)


@time_router.message(F.text, WaitChannelId.wait_input_time)
async def get_time(msg: Message, state: FSMContext):
    is_valid = await time_validation(msg.text)
    data = await state.get_data()
    channel_id = data.get('channel_id')
    channel_name = data.get('channel_name')
    buttons = InlineKeyboardMarkup(inline_keyboard=await back_button(channel_id, channel_name))
    if is_valid:
        times = await times_db.get_times(channel_id)
        target_time = datetime.strptime(msg.text, '%H:%M').strftime('%H:%M')
        if target_time in times:
            await msg.answer(
                "Произошла ошибка,такое время уже существует для текущего канала,попробуй заново или вернись  в меню",
                reply_markup=buttons)
        else:
            await times_db.set_time(channel_id=channel_id, target_time=target_time)
            await msg.answer("Время установлено успешно", reply_markup=buttons)
            await state.clear()
    else:
        await msg.answer("Произошла ошибка, попробуй заново или вернись  в меню", reply_markup=buttons)


@time_router.callback_query(F.data.startswith(("backToTimes")))
async def back_to_time_menu(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    channel_name = data[2]
    await show_times_menu(call, channel_id, channel_name)


@time_router.callback_query(F.data.startswith(("delTime")))
async def request_to_delete_time(call: CallbackQuery):
    data = call.data.split('_')
    time_to_del = data[1]
    channel_id = data[2]
    channel_name = data[3]
    buttons = InlineKeyboardMarkup(
        inline_keyboard=await agree_to_delete_time(time_to_delete=time_to_del, channel_id=channel_id,
                                                   channel_name=channel_name))
    await call.message.edit_text(f"Ты уверен что хочешь удалить данное время с канала {channel_name}",
                                 reply_markup=buttons)


@time_router.callback_query(F.data.startswith(("approveToDelTime")))
async def del_time(call: CallbackQuery):
    data = call.data.split('_')
    channel_id = data[1]
    time_to_del = data[2]
    channel_name = data[3]
    buttons = InlineKeyboardMarkup(inline_keyboard=await back_button(channel_id=channel_id, channel_name=channel_name))
    try:
        await times_db.delete_time(channel_id=channel_id, time_to_del=time_to_del)
        await call.message.edit_text("Время удалено успешно", reply_markup=buttons)
    except:
        await call.message.edit_text("Ошибка удаления", reply_markup=buttons)
