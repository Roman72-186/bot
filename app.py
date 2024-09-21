import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode


from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from middlewares.db import DataBaseSession

from database.engine import create_db, drop_db, session_maker


# from hendlers.group import user_group
from common.bot_cmds__list import private


ALLOWED_UPDATES = ['message, edited_updates']

bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher()
from hendlers.user import user_router

# user_router.message.outer_middleware(DataBaseSession())

dp.include_router(user_router)

# dp.include_router(user_group)

async def on_startup(bot):
    
    run_param = False
    if run_param: 
        await drop_db()
        
    await create_db()

async def on_shutdown(bot):
    print('БОТ ЛЕГ')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    
    
asyncio.run(main())