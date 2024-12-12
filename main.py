""" Основной файл для запуска ТГ бота.

Функциональность:
- Создание логирования.
- Создание функции для запуска бота, которая загружает конфигурацию из файла config.
- Регистрация роутеров и создание ссылки на экземпляр созданного бота через диспетчер.
- Запуск базы данных SQLite3.

Используются следующие модули:
- aiogram для работы с Telegram API.
- logging для ведения логов.
- config_data.config для загрузки конфигурации.
- handlers для обработки сообщений и состояний.
- keyboards.main_menu для настройки главного меню бота.
- database.sqlite3 для работы с базой данных.

Основные шаги:
1. Настройка логгера.
2. Загрузка конфигурации.
3. Создание экземпляра бота.
4. Настройка главного меню.
5. Подключение и запуск базы данных.
6. Регистрация роутеров в диспетчере.
7. Запуск polling для обработки обновлений.
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from handlers import fsm, user_handlers, other_handlers
from keyboards.main_menu import set_main_menu
from database.sqlite3 import db_start

bots = Bot

    
"""Функция запуска бота """
async def main():
    logging.basicConfig(
        filename='bot.log',
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logging.info(f'Start run bot')       
        
    # Загружаем конфиг в переменную config
    config: Config = load_config()
    
    # создаем экзмепляр Бота 
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    dp['bot_tg'] = bot # передаем экземпляр бота, для получения его из роутеров в других модулях
    
    # Настраиваем главное меню бота
    await set_main_menu(bot)
   
    # Загружаем базу данных и запускаем ее
    await db_start()
    logging.info(f'db activet')
  
    # Регистриуем роутеры в диспетчере
    dp.include_router(fsm.r)
    dp.include_router(user_handlers.r)
    dp.include_router(other_handlers.r)

    # Пропускаем накопившиеся updates и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    
if __name__ == "__main__":
    asyncio.run(main())
    
    