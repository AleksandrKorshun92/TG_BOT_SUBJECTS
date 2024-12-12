"""Функция для настройки кнопок основного меню (команд) Telegram-бота.

Эта функция принимает объект aiogram.Bot и устанавливает список команд, используя словарь 
LEXICON_COMMANDS из модуля lexicon.lexicon.
"""

from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon import LEXICON_COMMANDS


# Функция для настройки кнопки Menu бота (комманды)
async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command,
        description in LEXICON_COMMANDS.items()]
    await bot.set_my_commands(main_menu_commands)
