from symtable import Class
from time import process_time_ns
import json
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

import admin
import config
import text


def menu_update():
    main_topic = list(config.get_topic().keys())
    menu = []
    menu.clear()
    for i in range(0, len(config.get_topic()), 2):
        if i+1<len(config.get_topic()):
            menu.append([InlineKeyboardButton(text=main_topic[i], callback_data=f'topic_{main_topic[i]}'), InlineKeyboardButton(text=main_topic[i + 1], callback_data=f'topic_{main_topic[i + 1]}')])
        else:
            menu.append([InlineKeyboardButton(text=main_topic[i], callback_data=f'topic_{main_topic[i]}')])
    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu


def menu_admin():
    main_topic = list(config.get_topic().keys())
    menu1 = []
    menu1.clear()
    for i in range(0, len(config.get_topic()), 2):
        if i+1<len(config.get_topic()):
            menu1.append([InlineKeyboardButton(text=main_topic[i], callback_data=f'admin_{main_topic[i]}'), InlineKeyboardButton(text=main_topic[i + 1], callback_data=f'admin_{main_topic[i + 1]}')])
        else:
            menu1.append([InlineKeyboardButton(text=main_topic[i], callback_data=f'admin_{main_topic[i]}')])
    menu1 = InlineKeyboardMarkup(inline_keyboard=menu1)
    return menu1

def subtopic_create():

    menu_subtopic = []
    menu_subtopic.clear()
    main_topic = list(config.get_topic().keys())
    for i in range(0, len(config.get_topic()), 2):
        if i+1<len(config.get_topic()):
            menu_subtopic.append([InlineKeyboardButton(text=main_topic[i], callback_data=f'sub_admin_{main_topic[i]}'), InlineKeyboardButton(text=main_topic[i + 1], callback_data=f'sub_admin_{main_topic[i + 1]}')])
        else:
            menu_subtopic.append([InlineKeyboardButton(text=main_topic[i], callback_data=f'sub_admin_{main_topic[i]}')])
    menu_subtopic = InlineKeyboardMarkup(inline_keyboard=menu_subtopic)
    return menu_subtopic



def subtopic_get(user_id):
    menu_subtopic = []
    menu_subtopic.clear()
    subtopic = list(config.get_subtopic(admin.user_data[user_id]["get_topic"]).keys())
    main_topic = list(config.get_subtopic(admin.user_data[user_id]["get_topic"]).keys())
    print(subtopic)
    for i in range(0, len(main_topic), 2):
        if i + 1 < len(subtopic):
            menu_subtopic.append([InlineKeyboardButton(text=main_topic[i], callback_data=f's_{main_topic[i]}'),
                                  InlineKeyboardButton(text=main_topic[i + 1],
                                                       callback_data=f's_{main_topic[i + 1]}')])
        else:
            menu_subtopic.append([InlineKeyboardButton(text=main_topic[i], callback_data=f's_{main_topic[i]}')])
    menu_subtopic = InlineKeyboardMarkup(inline_keyboard=menu_subtopic)
    return menu_subtopic

exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])


admin_menu = [
[InlineKeyboardButton(text=text.add_task_text, callback_data="add_task")],
    [InlineKeyboardButton(text=text.create_topic_text, callback_data="create_topic")]
]

admin_menu = InlineKeyboardMarkup(inline_keyboard=admin_menu)

