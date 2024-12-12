"""Модуль для реализации конечного автомата (Finite State Machine, FSM) для процесса регистрации пользователя и
ввода предметов ЕГЭ с балами.

Этот модуль использует библиотеку aiogram для работы с Telegram-ботами и реализует FSM для сбора 
данных пользователя.

Основные компоненты модуля:
- MemoryStorage: Хранилище для сохранения состояний FSM.
- Router: Объект маршрутизации для регистрации обработчиков событий.
- FSMFillForm: Класс состояний для FSM, определяющий возможные состояния.
- process_start_registracio: Обработчик начала процесса регистрации.
- process_cancel_command: Обработчик отмены команды в состоянии по умолчанию.
- process_cancel_command_state: Обработчик отмены команды в любом другом состоянии.
- process_name_sent: Обработчик получения корректного имени.
- warning_not_first_name: Обработчик получения некорректного имени.
- process_save_profile: Обработчик завершения процесса регистрации и сохранения данных пользователя.
- warning_not_last_name: Обработчик получения некорректной фамилии.
- make_enter_name_subject - Обработчик начала процесса заполнения данных по предметам.
- make_enter_points_subject: Обработчик получения корректного названия предмета.
- warning_not_name_subject: Обработчик получения некорректного названия предмета.
- process_save_subject: Обработчик завершения процесса ввода предмета, баллов и сохранения данных.
- warning_not_points_subject: Обработчик получения некорректных баллов.
"""


import logging
from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message
from filters.regisration import RegistrationFilter
from lexicon.lexicon import LEXICON
from database.sqlite3 import create_profile, create_educational_subjects
from handlers.user_handlers import login_menu


# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()

# Создаем объекты роутера
r = Router()

# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    first_name = State()        # Состояние ожидания ввода имени
    last_name = State()         # Состояние ожидания ввода фамилии
    name_subject = State()      # Состояние ожидания ввода предмета
    points_subject = State()     # Состояние ожидания ввода баллов по предмету


# Будет срабатывать на команду /registracio или кнопку из меню start_reg и при отсутствии ранее регистрации 
# (проверка через RegistrationFilter) предлагает перейти к заполнению анкеты
@r.callback_query(F.data.in_(['start_reg']), StateFilter(default_state), RegistrationFilter())
@r.message(Command(commands='register'), StateFilter(default_state), RegistrationFilter())
async def process_start_registracio(event, state: FSMContext):
    logging.info(f'start FSM register')
    # проверяем вызов через кнопку или через команду
    if isinstance(event, CallbackQuery):
        await event.message.delete()
        await event.message.answer(text=LEXICON['input_first_name'])
    
    elif isinstance(event, Message):
        await event.answer(text=LEXICON['input_first_name'])
    else:
        raise ValueError(f"Неизвестный тип события: {type(event)}")

    # после переходит FSN стостояние - ввод имени
    await state.set_state(FSMFillForm.first_name)
     
            
# Будет срабатывать на команду "/cancel" в любых состояниях, кроме состояния по умолчанию, и отключать FSM состояний
@r.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['cancel'])
    
    # Сбрасываем FSM состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Будет срабатывать, если введено корректное имя и переводить в состояния ожидания ввода фамилии
@r.message(StateFilter(FSMFillForm.first_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    logging.info(f'start FSM first name')
    # Cохраняем введенное имя в хранилище по ключу "first_name"
    await state.update_data(first_name=message.text)
    await message.answer(text=LEXICON['input_last_name'])
    
    # Устанавливаем состояние ожидания ввода фамилии
    await state.set_state(FSMFillForm.last_name)


# Будет срабатывать, если во время ввода имени будет введено что-то некорректное
@r.message(StateFilter(FSMFillForm.first_name))
async def warning_not_first_name(message: Message):
    logging.info(f'start FSM error first name')
    await message.answer(text= LEXICON['error_first_name'])


# Будет срабатывать, если данные фамилии введены корректно
@r.message(StateFilter(FSMFillForm.last_name),F.text.isalpha())
async def process_save_profile(message: Message, state: FSMContext):
    logging.info(f'start FSM last name')
    # Cохраняем фамилию в хранилище по ключу "last_name"
    await state.update_data(last_name=message.text)
    
    # в БД создается запись с данными пользователя
    await create_profile(await state.get_data(), user_id= message.from_user.id)
    
    # Завершаем машину состояний FSM
    await state.clear()
    await message.answer(text=LEXICON['cancel_input_FSM'])
    await login_menu(message)
 

# Будет срабатывать, если во время ввода фамилии будет введено что-то некорректное
@r.message(StateFilter(FSMFillForm.last_name))
async def warning_not_last_name(message: Message):
    logging.info(f'start FSM error last name')
    await message.answer(text= LEXICON['error_last_name'])


#Будет переведен в состояние ожидания ввода данных для записи предмета ЕГЭ и баллов
@r.message(Command(commands='enter_scores'), StateFilter(default_state))
async def make_enter_name_subject(message: Message, state: FSMContext):
    logging.info(f'start FSM enter scores')
    await message.delete()
    await message.answer(text=LEXICON['input_name_subject'])
    # Устанавливаем состояние ожидания написания текста записи предмета
    await state.set_state(FSMFillForm.name_subject)
    
    
# Будет срабатывать, если корректное название предмета и переводить в статус ввода баллов по предмету
@r.message(StateFilter(FSMFillForm.name_subject),F.text.isalpha())
async def make_enter_points_subject(message: Message, state: FSMContext):
    logging.info(f'start FSM name subject')
    # Cохраняем введенное название предмета в хранилище по ключу "name_subject"
    await state.update_data(name_subject=message.text)
    await message.answer(text=LEXICON['input_points_subject'])
    
    # Устанавливаем состояние ожидания ввода баллов по ЕГЭ
    await state.set_state(FSMFillForm.points_subject)    
    

# Будет срабатывать, если во время ввода предмета будет введено что-то некорректное
@r.message(StateFilter(FSMFillForm.name_subject))
async def warning_not_name_subject(message: Message):
    logging.info(f'start FSM error name subject')
    await message.answer(text= LEXICON['error_name_subject'])    


# Будет срабатывать, если введены корректные данные по баллам ЕГЭ (число от 0 до 100)
@r.message(StateFilter(FSMFillForm.points_subject),
           lambda x: x.text.isdigit() and 0 <= int(x.text) <= 100)
async def process_save_subject(message: Message, state: FSMContext):
    logging.info(f'start FSM points subject')
    # Cохраняем баллы ЕГЭ в хранилище по ключу "points_subject"
    await state.update_data(points_subject=int(message.text))
    # в БД создается запись предмета с баллами
    await create_educational_subjects(await state.get_data(), user_id= message.from_user.id)
        
    # Завершаем машину состояний FSM
    await state.clear()
    await message.answer(text=LEXICON['cancel_input_FSM'])
    await login_menu(message)
    
  
# Будет срабатывать, если во время ввода баллов по ЕГЭ будет введено что-то некорректное
@r.message(StateFilter(FSMFillForm.points_subject))
async def warning_not_points_subject(message: Message):
    logging.info(f'start FSM error points subject')
    await message.answer(text=LEXICON['error_points_subject'])    
    
    
