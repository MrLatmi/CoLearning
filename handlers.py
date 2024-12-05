from aiogram import types, F, Router
from aiogram.types import Message, InputFile
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import flags
from states import Gen
from pathlib import Path

import random
import kb
import text
import re


router = Router()



@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu_update())


@router.message(F.text == "Меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu_update())

@router.callback_query(F.data.startswith('topic_'))
async def process_callback_topic(callback_query: types.CallbackQuery, state: FSMContext):
    topic_category = (callback_query.data.replace('topic_', ''))
    difficult_menu = [
        [InlineKeyboardButton(text="1", callback_data=f'difficult_1_{topic_category}'),
         InlineKeyboardButton(text="2", callback_data=f'difficult_2_{topic_category}'),
         InlineKeyboardButton(text="3", callback_data=f'difficult_3_{topic_category}')]
    ]
    difficult_menu = InlineKeyboardMarkup(inline_keyboard=difficult_menu)
    await state.clear()
    await callback_query.answer()
    await callback_query.message.answer(text.difficult, reply_markup=difficult_menu)
    await state.set_state(Gen.text_prompt)

@router.callback_query(F.data.startswith('difficult_'))
async def process_callback_difficult(callback_query: types.CallbackQuery, state: FSMContext):
    difficult_number = re.search(r'\d+', callback_query.data).group()
    topic_category = (callback_query.data.replace(f'difficult_{difficult_number}_', ''))
    await callback_query.answer()



    folder = f'tasks/{topic_category}/{difficult_number}/1.jpg'
    folderPath = Path(f'tasks/{topic_category}/{difficult_number}/')

    #task_number = random.randint(1, len(list(folderPath.iterdir())))


    if len(list(folderPath.iterdir())) != 0:
        task = FSInputFile(folder)
        await callback_query.message.answer_photo(task,"Задача")
    else:
        await callback_query.message.answer(text.no_files_in_directory)



@router.message(Gen.text_prompt)
async def generate_text(msg: Message, state: FSMContext):
    if msg.text == "Да":
        await msg.answer("Оке")