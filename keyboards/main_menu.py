from aiogram import Bot
from aiogram.types import BotCommand

comands = {}


async def set_main_menu(bot: Bot):
    main_menu = [BotCommand(command=k, description=v) for k, v in comands.items()]
    await bot.set_my_commands(main_menu)
