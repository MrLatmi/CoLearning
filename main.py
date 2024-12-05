import asyncio
import logging
import os.path

from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram.enums import ContentType
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware



from aiogram.types import Message, InputFile
from aiogram.filters import Command, state
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import flags

import kb
import text
from states import Gen
from admin import user_data


import config
from handlers import router
from admin import admin_router
from states import Gen

admins = [5358543785]
bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    dp.include_router(admin_router)
    dp.message.middleware(ChatActionMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


@admin_router.message(Gen.photo_task_getter, F.content_type.in_({'photo'}))
async def generate_text(msg: Message, state: FSMContext):
    user_id = msg.from_user.id

    if user_id in user_data and "get_topic" in user_data[user_id] and "subtopic" in user_data[user_id] and "task_type" in user_data[user_id] and "task_difficult" in user_data[user_id] and "get_name" in user_data[user_id] and "answer" in user_data[user_id] and "solving" in user_data[user_id] and "source" in user_data[user_id]:
        photo = msg.photo[-1]
        file_id = photo.file_id
        file_name = f'{user_data[user_id]["get_name"]}.jpg'
        path = f'tasks/{user_data[user_id]["get_topic"]}/{user_data[user_id]["subtopic"]}/{user_data[user_id]["task_type"]}/{user_data[user_id]["task_difficult"]}/'
        config.add_task(user_data[user_id]["get_topic"], user_data[user_id]["subtopic"], user_data[user_id]["get_name"], user_data[user_id]["answer"], user_data[user_id]["solving"], user_data[user_id]["source"], path)
        await  bot.download(file=msg.photo[-1].file_id, destination=os.path.join(f'tasks/{user_data[user_id]["get_topic"]}/{user_data[user_id]["subtopic"]}/{user_data[user_id]["task_type"]}/{user_data[user_id]["task_difficult"]}/', file_name))
        await state.clear()
        await msg.answer(text.successful_adding, reply_markup=kb.admin_menu)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

