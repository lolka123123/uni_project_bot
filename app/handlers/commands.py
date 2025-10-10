from aiogram import Router
from aiogram.types import Message, InputMediaAudio, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, update, desc, insert

from app.data.loader import bot
from app.database.settings import SessionLocal
from app.database import tables
from app.keyboards import reply
from app.localization.settings import get_translate

router = Router()



@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    if message.chat.id == message.from_user.id:
        await state.clear()
        await message.answer(get_translate('start_button'), reply_markup=reply.start_buttons())



# @router.message(Command('test'))
# async def test(message: Message):
#     async with SessionLocal() as session:
#         user = tables.Admin(user_id=message.from_user.id)
#         session.add(user)
#         await session.commit()
#         await session.refresh(user)

@router.message(Command('list'))
async def list(message: Message):
    chat_id = message.chat.id


    value = message.text.strip().lower().split(' ')

    async with SessionLocal() as session:
        files = []

        if len(value) < 2:
            result = await session.execute(select(tables.Audio).order_by(desc(tables.Audio.id)))
        else:
            result = await session.execute(select(tables.Audio).order_by(desc(tables.Audio.id)).join(tables.Audio.tags).where(
                tables.Tag.name == value[1]
            ))

        page_from, page_to = 0, 5
        if len(value) > 2:
            try:
                page = int(value[2])
                page_from, page_to = (page*5)-5, (page*5)
            except:
                page_from, page_to = 0, 5

        audios = result.scalars().all()[page_from:page_to]
        audios_names = {}

        for audio in audios:
            audios_names[audio.id] = audio.audio_name
            files.append(InputMediaAudio(media=FSInputFile(audio.audio_url, f'{audio.id}. {audio.audio_name}')))
            views = int(audio.views)
            await session.execute(update(tables.Audio).where(tables.Audio.id == audio.id).values(views=views + 1))
            await session.commit()
    if files:
        await bot.send_media_group(chat_id, files, reply_to_message_id=message.message_id)
        text = 'id ---- audios_name\n'
        for k, v in audios_names.items():
            text += f'{k}. {v}\n'
        await message.answer(text)
    else:
        await message.reply(get_translate('nothing'))





@router.message(Command('help'))
async def help(message: Message, state: FSMContext):
    await message.answer(get_translate('command_help_text'))


@router.message(Command('admin'))
async def admin(message: Message, state: FSMContext):
    async with SessionLocal() as session:
        user = await session.execute(select(tables.Admin).where(tables.Admin.user_id == message.from_user.id))
        user = user.scalar_one_or_none()
        if not user:
            admin = tables.Admin(user_id=message.from_user.id)
            session.add(admin)
            await session.commit()
            await session.refresh(admin)