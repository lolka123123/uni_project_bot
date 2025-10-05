from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

import os

from app.database.settings import SessionLocal
from app.database import tables
from app.data import states
from app.keyboards import inline

router = Router()




@router.callback_query(F.data)
async def audio_settings(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    if data[0] == 'audioAddTag':
        audio_id = int(data[-1])
        await state.set_state(states.AudioSettings.add_tag)
        msg = await call.message.answer('Введите новый тег: ', reply_markup=inline.cancel_markup())
        # msg = await bot.send_message(chat_id=call.message.chat.id, text='Введите тег: ', reply_markup=inline.cancel_markup(audio_id))
        await state.update_data(audio_id=audio_id, message_id=msg.message_id)
    elif data[0] == 'audioRemoveTag':
        audio_id = int(data[-1])
        await state.set_state(states.AudioSettings.remove_tag)
        msg = await call.message.answer('Введите тег: ', reply_markup=inline.cancel_markup())
        await state.update_data(audio_id=audio_id, message_id=msg.message_id)
    elif data[0] == 'audioRemoveAudio':
        audio_id = int(data[-1])
        await call.message.edit_caption(caption='Вы точно хотите удалить?', reply_markup=inline.delete_audio(audio_id))


    elif data[0] == 'cancel':
        await call.message.delete()
        await state.clear()



    elif data[0] == 'deleteAudioCancel':
        audio_id = int(data[-1])
        async with SessionLocal() as session:
            audio = await session.execute(select(tables.Audio).where(tables.Audio.id == audio_id).options(selectinload(
                tables.Audio.tags)))
            audio = audio.scalar_one_or_none()

            if not audio:
                await call.message.delete()
                return

            audio_tags_list = [tag.name for tag in audio.tags]
            audio_tags = ''
            for tag in audio_tags_list:
                audio_tags += f'{tag} '
        await call.message.edit_caption(caption=f'Теги: {audio_tags}', reply_markup=inline.edit_audio(audio_id))
    elif data[0] == 'deleteAudio':
        audio_id = int(data[-1])
        async with SessionLocal() as session:
            await session.execute(delete(tables.Audio).where(tables.Audio.id == audio_id))
            await session.commit()
        await call.message.delete()




    elif data[0] == 'audioCut':
        audio_id = int(data[-1])
        await state.set_state(states.CutAudio.cut_from)
        msg = await call.message.answer('Обрезать от:\nПример: минуты->1.42<-секунды', reply_markup=inline.cancel_markup())
        await state.update_data(audio_id=audio_id, previous_message_id=msg.message_id)
    elif data[0] == 'cutSave':
        audio_id = int(data[1])
        random_name = int(data[2])
        async with SessionLocal() as session:
            audio = await session.execute(select(tables.Audio).where(tables.Audio.id == audio_id))
            audio = audio.scalar_one()
            audio_url = audio.audio_url
            os.replace(f'app/media/cut/{random_name}.mp3', audio_url)
            await call.message.edit_caption('Сохранено', reply_markup=inline.empty())

