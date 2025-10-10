from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.localization.settings import get_translate

def start_buttons():

    buttons = [
        [KeyboardButton(text=get_translate('reply_edit_audio'))],
        [KeyboardButton(text=get_translate('reply_tag_list'))],
        [KeyboardButton(text=get_translate('reply_remove_tag'))],
    ]

    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return markup