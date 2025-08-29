from aiogram.filters.state import State, StatesGroup


class WaitChannelId(StatesGroup):
    wait_id = State()
    wait_input_time = State()
