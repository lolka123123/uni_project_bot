from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def empty():
    return InlineKeyboardMarkup(inline_keyboard=[[]])
def cancel_markup():

    cancel = InlineKeyboardButton(text='Cancel', callback_data=f'cancel')
    buttons = [[cancel]]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup
def edit_audio(audio_id):

    cut = InlineKeyboardButton(text='Cut', callback_data=f'audioCut_{audio_id}')
    remove = InlineKeyboardButton(text='Remove audio', callback_data=f'audioRemoveAudio_{audio_id}')
    add_tag = InlineKeyboardButton(text='Add tag', callback_data=f'audioAddTag_{audio_id}')
    remove_tag = InlineKeyboardButton(text='Remove tag', callback_data=f'audioRemoveTag_{audio_id}')
    # cancel = InlineKeyboardButton(text='Cancel', callback_data=f'audioCancel_{audio_id}')

    buttons = [[cut, remove],
               [add_tag, remove_tag]]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup

def delete_audio(audio_id):
    buttons = [[InlineKeyboardButton(text='Delete', callback_data=f'deleteAudio_{audio_id}')],
               [InlineKeyboardButton(text='Cancel', callback_data=f'deleteAudioCancel_{audio_id}')]]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def cut_audio(audio_id, audio_name):
    buttons = [[InlineKeyboardButton(text='Save', callback_data=f'cutSave_{audio_id}_{audio_name}')],
               [InlineKeyboardButton(text='Cancel', callback_data=f'cancel')]]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup
