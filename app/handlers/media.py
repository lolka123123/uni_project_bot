from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select

import os

from app.data.loader import bot
from app.database.settings import SessionLocal
from app.database import tables
from app.localization.settings import get_translate

from random import randint

router = Router()


@router.message(F.audio)
async def get_audio(message: Message):
    file_id = message.audio.file_id
    file_name = message.audio.file_name
    file = await bot.get_file(file_id)

    while os.path.exists(f'app/media/audios/{file_name}'):
        file_name = f'{randint(0, 9)}{file_name}'

    save_dir = "app/media/audios"
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, file_name)

    await bot.download_file(file.file_path, destination=save_path)

    tags = []
    bot_info = await bot.get_me()
    if message.caption:
        for tag in message.caption.lower().strip().split(' '):
            if f'@{bot_info.username.lower()}' in tag:
                continue
            tags.append(tag)

    async with SessionLocal() as session:
        if tags:
            for tag_name in tags:
                result = await session.execute(select(tables.Tag).where(tables.Tag.name == tag_name))
                tag = result.scalar_one_or_none()
                if not tag:
                    session.add(tables.Tag(name=tag_name))
            await session.commit()

        new_audio = tables.Audio(user_id=message.from_user.id, username=message.from_user.username,
                                 audio_url=save_path, audio_name=file_name)

        for tag_name in tags:
            result = await session.execute(
                select(tables.Tag).where(tables.Tag.name == tag_name)
            )
            tag = result.scalars().first()
            new_audio.tags.append(tag)

        session.add(new_audio)
        await session.commit()
        await session.refresh(new_audio)

        audio_id = new_audio.id


    tags_text = ''
    if tags:
        for tag in tags:
            tags_text += f'{tag} '
    await message.reply(f'id: {audio_id}\n{get_translate("get_audio_audio")}: {message.audio.file_name}\n'
                        f'{get_translate("get_audio_tags")}: {tags_text}\n{get_translate("get_audio_created")}')

