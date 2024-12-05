from aiogram import F, Router
from aiogram.types import Message
from config import ADMINS
from aiogram.utils.chat_action import ChatActionSender
import text
import kb
from states import Gen
import os
import re
import config
from aiogram import types, F, Router
from aiogram.types import Message, InputFile
from aiogram.filters import Command, state, StateFilter
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import flags
from states import Gen
from pathlib import Path
import aiohttp

admins = [int(admin_id) for admin_id in ADMINS.split(',')]
admin_router = Router()


@admin_router.message(F.text.endswith('Админ панель') & (F.from_user.id.in_(admins)))
async def get_profile(msg: Message):
        await msg.answer(text.admin_message, reply_markup=kb.admin_menu)

user_data ={}

@admin_router.callback_query(F.data == 'create_topic')
async def create_topic(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.answer(text.create_topic_name, reply_markup=kb.subtopic_create())
        await state.clear()
        await callback_query.answer()
        await state.set_state(Gen.name_getter)

@admin_router.callback_query(F.data.startswith('sub_admin_'))
async def process_callback_topic(callback_query: types.CallbackQuery, state: FSMContext):
    topic_category = (callback_query.data.replace('sub_admin_', ''))
    user_data[callback_query.from_user.id] = {"main_topic" : topic_category}
    await callback_query.message.answer(text.set_subtopic_name)
    await state.clear()
    await callback_query.answer()
    await state.set_state(Gen.subtopic_name_getter)

@admin_router.message(Gen.subtopic_name_getter)
async def get_profile(msg: Message, state: FSMContext):
        topic_name = msg.text
        user_id = msg.from_user.id
        if user_id in user_data and "main_topic" in user_data[user_id]:
            config.add_subtopic(user_data[user_id]["main_topic"], topic_name)

            path_main = f'tasks/{user_data[user_id]["main_topic"]}/{topic_name}'
            try:
                os.makedirs(path_main)
            except FileExistsError:
                print('Директория уже существует')




            for i in range(1, config.difficult_levels + 1):
                path_dif = f'tasks/{user_data[user_id]["main_topic"]}/{topic_name}/Качественные/{i}'
                try:
                    os.makedirs(path_dif)
                except FileExistsError:
                    print('Директория уже существует')

            for i in range(1, config.difficult_levels + 1):
                path_dif = f'tasks/{user_data[user_id]["main_topic"]}/{topic_name}/Смешанные/{i}'
                try:
                    os.makedirs(path_dif)
                except FileExistsError:
                    print('Директория уже существует')

            for i in range(1, config.difficult_levels + 1):
                path_dif = f'tasks/{user_data[user_id]["main_topic"]}/{topic_name}/Вычислительные/{i}'
                try:
                    os.makedirs(path_dif)
                except FileExistsError:
                    print('Директория уже существует')

@admin_router.message(Gen.name_getter)
async def get_profile(msg: Message, state: FSMContext):
        topic_name = msg.text
        config.add_topic(topic_name)
        path_main = f'tasks/{topic_name}'
        try:
                os.makedirs(path_main)
        except FileExistsError:
                print('Директория уже существует')

        for i in range(1, config.difficult_levels + 1):
            path_dif = f'tasks/{topic_name}/Разное/Качественные/{i}'
            try:
                os.makedirs(path_dif)
            except FileExistsError:
                print('Директория уже существует')

        for i in range(1, config.difficult_levels + 1):
            path_dif = f'tasks/{topic_name}/Разное/Смешанные/{i}'
            try:
                os.makedirs(path_dif)
            except FileExistsError:
                print('Директория уже существует')

        for i in range(1, config.difficult_levels + 1):
            path_dif = f'tasks/{topic_name}/Разное/Вычислительные/{i}'
            try:
                os.makedirs(path_dif)
            except FileExistsError:
                print('Директория уже существует')

        await state.clear()

@admin_router.callback_query(F.data == 'add_task')
async def create_topic(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer(text.create_topic_name, reply_markup= kb.menu_admin())
    await state.clear()
    await callback_query.answer()

@admin_router.callback_query(F.data.startswith('admin_'))
async def process_callback_topic(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()

    topic_category = (callback_query.data.replace('admin_', ''))

    await state.clear()
    await callback_query.answer()

    user_data[callback_query.from_user.id] = {"get_topic":topic_category}

    await callback_query.message.answer(text.difficult, reply_markup=kb.subtopic_get(callback_query.from_user.id))
    await state.set_state(Gen.text_prompt)


@admin_router.callback_query(F.data.startswith('s_'))
async def process_callback_type(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if user_id in user_data and "get_topic" in user_data[user_id]:
        await callback_query.message.delete()
        sub_topic = (callback_query.data.replace(f's_', ''))
        user_data[callback_query.from_user.id]["subtopic"] = sub_topic
        difficult_menu = [
            [InlineKeyboardButton(text=text.quality_task_text, callback_data=f'tp_{text.quality_task_text}'),
            InlineKeyboardButton(text=text.calculating_task_text, callback_data=f'tp_{text.calculating_task_text}')],
            [InlineKeyboardButton(text=text.mixed_task_text, callback_data=f'tp_{text.mixed_task_text}')]
        ]
        difficult_menu = InlineKeyboardMarkup(inline_keyboard=difficult_menu)
        await callback_query.message.answer(text.task_type_choose, reply_markup=difficult_menu)
        await callback_query.answer()



@admin_router.callback_query(F.data.startswith('tp_'))
async def process_callback_difficult(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()

    user_id = callback_query.from_user.id
    if user_id in user_data and "get_topic" in user_data[user_id] and "subtopic" in user_data[
        user_id]:
        task_type = (callback_query.data.replace(f'tp_', ''))
        user_data[callback_query.from_user.id]["task_type"] = task_type
        difficult_menu = [
        [InlineKeyboardButton(text="1", callback_data=f'ad_dif_1'),
        InlineKeyboardButton(text="2", callback_data=f'ad_dif_2'),
        InlineKeyboardButton(text="3", callback_data=f'ad_dif_3')],
        [InlineKeyboardButton(text="4", callback_data=f'ad_dif_4'),
        InlineKeyboardButton(text="5", callback_data=f'ad_dif_5'),
        InlineKeyboardButton(text="6", callback_data=f'ad_dif_6')]]
        difficult_menu = InlineKeyboardMarkup(inline_keyboard=difficult_menu)
        await callback_query.message.answer(text.task_difficult_choose, reply_markup=difficult_menu)

    await callback_query.answer()


@admin_router.callback_query(F.data.startswith('ad_dif_'))
async def process_callback_difficult(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if user_id in user_data and "get_topic" in user_data[user_id] and "subtopic" in user_data[
        user_id] and "task_type" in user_data[user_id]:
        await callback_query.message.delete()
        difficult_number = (callback_query.data.replace(f'ad_dif_', ''))
        user_data[callback_query.from_user.id]["task_difficult"] = difficult_number
        await state.set_state(Gen.task_name_getter)
        await callback_query.message.answer(text.task_name_send)

@admin_router.message(StateFilter(Gen.task_name_getter))
async def name_getter(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    if user_id in user_data and "get_topic" in user_data[user_id] and "subtopic" in user_data[user_id] and "task_type" in user_data[user_id] and "task_difficult" in user_data[user_id]:
        user_data[user_id]["get_name"] = msg.text

        await msg.answer(text.task_answer_send)
        await state.set_state(Gen.answer_task_getter)

@admin_router.message(StateFilter(Gen.answer_task_getter))
async def name_getter(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    if user_id in user_data and "get_topic" in user_data[user_id] and "subtopic" in user_data[user_id] and "task_type" in user_data[user_id] and "task_difficult" in user_data[user_id] and "get_name" in user_data[user_id]:
        user_data[user_id]["answer"] = msg.text

        await msg.answer(text.task_solution_send)
        await state.set_state(Gen.solving_getter)



@admin_router.message(StateFilter(Gen.solving_getter))
async def name_getter(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    if user_id in user_data and "get_topic" in user_data[user_id] and "subtopic" in user_data[user_id] and "task_type" in user_data[user_id] and "task_difficult" in user_data[user_id] and "get_name" in user_data[user_id] and "answer" in user_data[user_id]:
        user_data[user_id]["solving"] = msg.text

        await msg.answer(text.task_source_send)
        await state.set_state(Gen.source_getter)


@admin_router.message(StateFilter(Gen.source_getter))
async def name_getter(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    if user_id in user_data and "get_topic" in user_data[user_id] and "subtopic" in user_data[user_id] and "task_type" in user_data[user_id] and "task_difficult" in user_data[user_id] and "get_name" in user_data[user_id] and "answer" in user_data[user_id] and "solving" in user_data[user_id]:
        user_data[user_id]["source"] = msg.text

        await msg.answer(text.task_photo_send)
        await state.set_state(Gen.photo_task_getter)



