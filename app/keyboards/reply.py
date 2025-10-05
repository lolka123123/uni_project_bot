from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def start_buttons():

    buttons = [
        [KeyboardButton(text='Edit audio')],
        [KeyboardButton(text='Tag list')],
        [KeyboardButton(text='Remove tag')],
    ]

    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return markup