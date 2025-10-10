from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.localization.settings import get_translate

def empty():
    return InlineKeyboardMarkup(inline_keyboard=[[]])
def cancel_markup():

    cancel = InlineKeyboardButton(text=get_translate("inline_cancel"), callback_data=f'cancel')
    buttons = [[cancel]]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup
def edit_audio(audio_id):

    cut = InlineKeyboardButton(text=get_translate("inline_cut"), callback_data=f'audioCut_{audio_id}')
    remove = InlineKeyboardButton(text=get_translate("inline_remove_audio"), callback_data=f'audioRemoveAudio_{audio_id}')
    add_tag = InlineKeyboardButton(text=get_translate("inline_add_tag"), callback_data=f'audioAddTag_{audio_id}')
    remove_tag = InlineKeyboardButton(text=get_translate("inline_remove_tag"), callback_data=f'audioRemoveTag_{audio_id}')
    # cancel = InlineKeyboardButton(text='Cancel', callback_data=f'audioCancel_{audio_id}')

    buttons = [[cut, remove],
               [add_tag, remove_tag]]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup

def delete_audio(audio_id):
    buttons = [[InlineKeyboardButton(text=get_translate("inline_delete"), callback_data=f'deleteAudio_{audio_id}')],
               [InlineKeyboardButton(text=get_translate("inline_cancel"), callback_data=f'deleteAudioCancel_{audio_id}')]]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def cut_audio(audio_id, audio_name):
    buttons = [[InlineKeyboardButton(text=get_translate("inline_save"), callback_data=f'cutSave_{audio_id}_{audio_name}')],
               [InlineKeyboardButton(text=get_translate("inline_cancel"), callback_data=f'cancel')]]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup
