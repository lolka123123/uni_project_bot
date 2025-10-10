from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload

import os
from random import randint

from app.data.loader import bot
from app.database.settings import SessionLocal
from app.database import tables
from app.data import states
from app.keyboards import inline
from app.localization.settings import get_translate

from app.cutAudio import cut_audio

router = Router()


@router.message(F.text, StateFilter(None))
async def main(message: Message, state: FSMContext):
    if message.chat.id == message.from_user.id:
        if message.text == get_translate('reply_edit_audio'):
            msg = await message.answer(get_translate('main_edit_audio_id'), reply_markup=inline.cancel_markup())
            await state.set_state(states.EditAudio.audio_id)
            await state.update_data(message_id=msg.message_id)
        elif message.text == get_translate('reply_tag_list'):
            async with SessionLocal() as session:
                tags = await session.execute(select(tables.Tag))
                tags = tags.scalars().all()
                tags_name = ''
                for tag in tags:
                    tags_name += f'{tag.name} '
                await message.answer(f'Все теги: \n{tags_name}')

        elif message.text == get_translate('reply_remove_tag'):
            msg = await message.answer(get_translate('main_input_tag_to_remove'), reply_markup=inline.cancel_markup())
            await state.set_state(states.RemoveTag.audio_id)
            await state.update_data(message_id=msg.message_id)



@router.message(F.text, states.EditAudio.audio_id)
async def edit_audio_id(message: Message, state: FSMContext):
    try:
        audio_id = int(message.text)
        async with SessionLocal() as session:
            audio = await session.execute(select(tables.Audio).where(tables.Audio.id == audio_id).options(selectinload(
                tables.Audio.tags)))
            audio = audio.scalar_one_or_none()
            if not audio:
                await message.answer(get_translate('audio_not_exist'))
            else:
                audio_url = audio.audio_url
                file = FSInputFile(audio_url)
                audio_tags_list = [tag.name for tag in audio.tags]
                audio_tags = ''
                for tag in audio_tags_list:
                    audio_tags += f'{tag} '

                data = await state.get_data()
                message_id = data['message_id']
                await bot.delete_message(message.chat.id, message_id)

                await state.clear()
                await bot.send_audio(chat_id=message.chat.id, audio=file, caption=f'{get_translate("audio_settings_delete_cancel_tags")}: {audio_tags}', reply_to_message_id=message.message_id, reply_markup=inline.edit_audio(audio_id))
    except:
        await message.answer(get_translate('audio_incorrect_id'))


@router.message(F.text, states.RemoveTag.audio_id)
async def remove_tag(message: Message, state: FSMContext):
    tag_name = message.text.lower()
    async with SessionLocal() as session:
        tag = await session.execute(select(tables.Tag).where(tables.Tag.name == tag_name))
        tag = tag.scalar_one_or_none()

        if not tag:
            await message.answer(f'{get_translate("tag_not_exists_1")} "{tag_name}" {get_translate("tag_not_exists_2")}')
        else:
            await session.execute(delete(tables.Tag).where(tables.Tag.id == tag.id))
            await session.commit()

            data = await state.get_data()
            message_id = data['message_id']
            await bot.delete_message(message.chat.id, message_id)

            await state.clear()
            await message.answer(f'{get_translate("tag_was_removed_1")} "{tag_name}" {get_translate("tag_was_removed_2")}')




@router.message(F.text, states.AudioSettings.add_tag)
async def audio_add_tag(message: Message, state: FSMContext):
    if ' ' in message.text:
        await message.answer(get_translate('tag_must_not_contain_spaces'))
    else:
        data = await state.get_data()
        audio_id = data['audio_id']
        call_message_id = data['message_id']

        async with SessionLocal() as session:
            audio = await session.execute(select(tables.Audio).where(tables.Audio.id == audio_id, tables.Audio.tags.any(
                tables.Tag.name == message.text.lower())))
            audio = audio.scalar_one_or_none()
            if audio:
                await message.answer(get_translate('tag_already_exists'))
            else:
                tag_name = message.text.lower()
                await bot.delete_message(message.chat.id, call_message_id)

                tag = await session.execute(select(tables.Tag).where(tables.Tag.name == tag_name))
                tag = tag.scalar_one_or_none()
                if not tag:
                    new_tag = tables.Tag(name=tag_name)
                    session.add(new_tag)
                    await session.commit()
                    await session.refresh(new_tag)

                tag_id = await session.execute(select(tables.Tag).where(tables.Tag.name == tag_name))
                tag_id = tag_id.scalar_one().id

                await session.execute(insert(tables.audio_tags).values(audio_id=audio_id, tag_id=tag_id))
                await session.commit()

                await state.clear()

                await message.answer(f'{get_translate("tag_was_added_1")} "{tag_name}" {get_translate("tag_was_added_2")}')
                # tag = await session.execute(select(tables.Tag).where())



@router.message(F.text, states.AudioSettings.remove_tag)
async def audio_remove_tag(message: Message, state: FSMContext):
    if ' ' in message.text:
        await message.answer(get_translate('tag_must_not_contain_spaces'))
    else:
        data = await state.get_data()
        audio_id = data['audio_id']
        call_message_id = data['message_id']

        async with SessionLocal() as session:
            audio = await session.execute(select(tables.Audio).where(tables.Audio.id == audio_id, tables.Audio.tags.any(
                tables.Tag.name == message.text)))
            audio = audio.scalar_one_or_none()
            if not audio:
                await message.answer(get_translate('object_does_not_have_this_tag'))
            else:
                await bot.delete_message(message.chat.id, call_message_id)
                tag_id = await session.execute(select(tables.Tag).where(tables.Tag.name == message.text))
                tag_id = tag_id.scalar_one().id

                await session.execute(delete(tables.audio_tags).where(tables.audio_tags.c.audio_id == audio_id).where(
                    tables.audio_tags.c.tag_id == tag_id))

                await session.commit()
                await state.clear()
                await message.answer(f'{get_translate("tag_was_removed_1")} "{message.text.lower()}" {get_translate("tag_was_removed_2")}')


@router.message(F.text, states.CutAudio.cut_from)
async def audio_cut_from(message: Message, state: FSMContext):
    try:
        timing = message.text.split('.')
        minutes = int(timing[0])
        seconds = int(timing[1])

        if minutes < 0 or seconds < 0:
            await message.answer(get_translate('time_can_not_be_negative'))
            return
        if seconds >= 60:
            await message.answer(get_translate('seconds_cannot_be_more_than'))
            return

        cut_from = [minutes, seconds]

        data = await state.get_data()
        previous_message_id = data['previous_message_id']
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=previous_message_id, reply_markup=inline.empty())


        msg = await message.answer(get_translate('cut_to'), reply_markup=inline.cancel_markup())
        await state.update_data(cut_from=cut_from, previous_message_id=msg.message_id)
        await state.set_state(states.CutAudio.cut_to)


    except Exception as e:
        print(e)
        await message.answer(get_translate('something_went_wrong'))

@router.message(F.text, states.CutAudio.cut_to)
async def audio_cut_to(message: Message, state: FSMContext):
    try:
        timing = message.text.split('.')
        minutes = int(timing[0])
        seconds = int(timing[1])

        if minutes < 0 or seconds < 0:
            await message.answer(get_translate('time_can_not_be_negative'))
            return
        if seconds >= 60:
            await message.answer(get_translate('seconds_cannot_be_more_than'))
            return

        cut_to = [minutes, seconds]



        data = await state.get_data()
        cut_from = data['cut_from']
        previous_message_id = data['previous_message_id']
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=previous_message_id, reply_markup=inline.empty())

        seconds_from = cut_from[0] * 60 + cut_from[1]
        seconds_to = cut_to[0] * 60 + cut_to[1]

        audio_id = data['audio_id']
        async with SessionLocal() as session:
            audio = await session.execute(select(tables.Audio).where(tables.Audio.id == audio_id))
            audio = audio.scalar_one()
            audio_url = audio.audio_url

            os.makedirs('app/media/cut', exist_ok=True)

            random_name = str(randint(0, 9999999))
            while os.path.exists(f'app/media/cut/{random_name}.mp3'):
                random_name = str(randint(0, 9999999))


            cut_audio(audio_url, seconds_from, seconds_to, f'app/media/cut/{random_name}.mp3')

            file = FSInputFile(f'app/media/cut/{random_name}.mp3')

            await state.clear()
            await bot.send_audio(message.chat.id, file, reply_markup=inline.cut_audio(audio_id, audio_name=random_name))
    except Exception as e:
        print(e)
        await message.answer(get_translate('something_went_wrong'))