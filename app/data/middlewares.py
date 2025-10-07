from aiogram import BaseMiddleware
from aiogram.types import Message

from typing import Callable, Awaitable, Dict, Any
from sqlalchemy import select

from app.data.loader import bot
from app.database.settings import SessionLocal
from app.database import tables


class AnswerIfHasTagMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       message: Message,
                       data: Dict[str, Any]) -> Any:
        if message.chat.id == message.from_user.id:
            # async with SessionLocal() as session:
            #     user = await session.execute(select(tables.Admin).where(tables.Admin.user_id == message.from_user.id))
            #     user = user.scalar_one_or_none()
            # if user:
            #     return await handler(message, data)
            return await handler(message, data) # ВРЕМЕННО!!!!! ПОТОМ НАДО УБРАТЬ
        else:
            bot_info = await bot.get_me()
            if (message.text and f'@{bot_info.username}' in message.text) or \
                (message.caption and f'@{bot_info.username}' in message.caption):
                return await handler(message, data)
            return


