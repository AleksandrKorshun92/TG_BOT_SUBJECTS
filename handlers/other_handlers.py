"""
Данный модуль реализует простую функциональность эхо-бота на основе библиотеки aiogram. 
Бот реагирует на входящие сообщения и команды пользователей, за исключением тех, которые указаны
обработаны в других handlers и в списке IGNORE_MESSAGES. 

Основные компоненты модуля:
1. Список игнорируемых сообщений:
   - Определен список IGNORE_MESSAGES, содержащий команды или сообщения, на которые бот не должен реагировать.

2. Обработчик сообщений:
   - Декорированная функция send_echo обрабатывает входящие сообщения. Она сначала проверяет, не содержится ли входящее сообщение в списке игнорируемых. 
   Если сообщение должно быть проигнорировано, функция завершается без выполнения дальнейших действий.
   - Если сообщение не игнорируется, оно сохраняется в базе данных с помощью функции update_message, после чего отправляется 
   обратно пользователю с использованием лексикона LEXICON.

"""

import logging
from aiogram import Router
from aiogram.types import Message
from database.sqlite3 import create_message
from lexicon.lexicon import LEXICON


r = Router()

# Список сообщений, на которые бот не отвечает
IGNORE_MESSAGES = ['/register']

@r.message()
async def send_echo(message: Message):
   logging.info(f'Start send echo - message')   
   # Проверка, находится ли сообщение в списке игнорируемых
   if message.text in IGNORE_MESSAGES:
      return  # Прекращаем выполнение функции, если сообщение должно быть проигнорировано
    
   # Запись в базу данных
   await create_message(message.text, message.from_user.id)
    
   # Ответ бота
   logging.info(f'message echo message')
   await message.answer(LEXICON['echo_message_bot'])

    
    
