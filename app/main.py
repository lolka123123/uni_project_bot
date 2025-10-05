import asyncio

from app.handlers import commands, text_handlers, media, callbacks
from app.data.loader import bot, dp
from app.data import middlewares
from app.database.settings import engine, Base




async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    dp.message.middleware(middlewares.AnswerIfHasTagMiddleware())

    dp.include_routers(
        commands.router,
        callbacks.router,
        media.router,
        text_handlers.router
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await engine.dispose()




if __name__ == '__main__':
    asyncio.run(main())