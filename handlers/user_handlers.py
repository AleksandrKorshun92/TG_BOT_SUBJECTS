"""Этот модуль реализует набор функций для управления взаимодействием с пользователями в рамках бота 
на платформе Telegram с использованием библиотеки aiogram. 
Модуль включает обработчики различных команд и действий пользователя, таких как начало работы с ботом,
авторизация, просмотр оценок по учебным дисциплинам.

Функции-обработчики:
   - start_menu: Обрабатывает команду /start, приветствует пользователя и предлагает выбрать между регистрацией и входом.
   - login_menu: Обрабатывает нажатие кнопки входа, проверяет наличие пользователя в базе данных и предлагает 
   зарегистрироваться, если он отсутствует.
   - process_help_command: Обрабатывает команду /help, предоставляя справочную информацию.
   - services_answer_command: Обрабатывает команду /view_scores, выводит оценки пользователя по различным предметам, 
   если они имеются в базе данных.
"""
import logging
from aiogram import F, Router
from aiogram.types import FSInputFile 
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import LEXICON
from keyboards.keybords import menu_login_or_reg, menu_reg_start
from database.sqlite3 import load_user, load_educational_subjects


r = Router()

# Будет срабатывать на команду /start 
# Приветствует пользователя по имени и предлагает выбрать между регистрацией и входом, используя клавиатуру menu_login_or_reg() 
@r.message(CommandStart())
async def start_bot(message: Message):
    logging.info(f'command start')
    await message.answer(text= f"{message.from_user.first_name} {LEXICON['start_reg']}", 
                             reply_markup=menu_login_or_reg())
      

# Будет срабатывать при нажатии кнопки входа в меню.  
# Если пользователь не найден, предлагается пройти регистрацию, найден - производит вход.
@r.callback_query(F.data.in_(['login']))
@r.message(F.data.in_(['login']))
async def login_menu(event):
    logging.info(f'callback login')
    # выгружает данные пользователя из БД по id 
    user_sql = await load_user(event.from_user.id)
    # Если нет пользователя в БД, то просим пройти регистрацию
    if not user_sql:
        logging.info(f'callback message no registration')
        await event.message.answer(text= 'Прости, ' + event.from_user.first_name +
                             LEXICON['start_no_reg'], 
                             reply_markup=menu_reg_start())
    
    else:
        logging.info(f'callback message login menu')
        # Определяем вызов функции был через команду или по кнопки
        if isinstance(event, CallbackQuery):
            await event.message.delete()
            await event.message.answer_photo(photo=FSInputFile('photo/login_true.jpeg', 
                                            filename='bot_start'),
                                            caption=f"Привет, {event.from_user.first_name}!\n {LEXICON['greeting']}")
        else: 
            await event.answer_photo(photo=FSInputFile('photo/login_true.jpeg', 
                                            filename='bot_start'),
                                            caption=f"Привет, {event.from_user.first_name}!\n {LEXICON['greeting']}")


# Будет срабатывать  на команду /help и показывать справку по боту
@r.message(Command(commands='help'))
async def process_help_command(message: Message):
    logging.info(f'commands help')
    await message.answer(text=LEXICON['help'])


# Будет срабатывать  на команду /view_scores и показывать данные по предметам и балам ЕГЭ
@r.message(Command(commands='view_scores'))
async def services_answer_command(message:Message):
    logging.info(f'commands view_scores')
    await message.delete()
    user_sql = await load_educational_subjects(message.from_user.id)
    # если записей нет, то указываем на отсутствие данных в базе по предметам
    if user_sql:
        logging.info(f'print subject')
        for subject in user_sql:
            await message.answer(text = f'Баллы по предмету {subject[1]} - {subject[2]}\n')
    else:
        logging.info(f'message not subject')
        await message.answer(text=f"{message.from_user.first_name} {LEXICON['not_subject']}")
   

    
