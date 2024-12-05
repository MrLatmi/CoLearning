from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):
    user_state = State()
    admin_state = State()
    answer_getter = State()
    text_prompt = State()
    img_getter = State()
    name_getter = State()
    photo_task_getter = State()
    subtopic_name_getter = State()
    task_name_getter = State()
    answer_task_getter = State()
    solving_getter = State()
    source_getter = State()
