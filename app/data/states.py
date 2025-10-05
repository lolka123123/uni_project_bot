from aiogram.fsm.state import State, StatesGroup


class EditAudio(StatesGroup):
    audio_id = State()

class RemoveTag(StatesGroup):
    audio_id = State()


class AudioSettings(StatesGroup):
    add_tag = State()
    remove_tag = State()
    remove_audio = State()

class CutAudio(StatesGroup):
    cut_from = State()
    cut_to = State()



