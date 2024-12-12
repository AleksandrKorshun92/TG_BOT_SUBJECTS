"""Этот модуль содержит функции, предназначенные для создания и возврата объектов инлайн-клавиатур.
Эти клавиатуры предоставляют пользователю возможность выбора действий, связанных с регистрацией и 
входом в систему.

### Основные компоненты модуля:
1. Функция menu_login_or_reg:
   - Создает инлайн-клавиатуру с двумя кнопками: одна для регистрации, другая для входа в аккаунт.
   - Возвращает объект InlineKeyboardMarkup, представляющий эту клавиатуру.

2. Функция menu_reg_start:
   - Создает инлайн-клавиатуру с одной кнопкой для начала процесса регистрации.
   - Возвращает объект InlineKeyboardMarkup, представляющий эту клавиатуру.

Эти функции используются в других частях приложения для предоставления пользователю интерфейсов, 
позволяющих выбирать между различными действиями.
"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# кнопки для входа или регистрации пользователя
def menu_login_or_reg():
    start_reg_button = InlineKeyboardButton(
        text='✅ Зарегестрироваться',
        callback_data='start_reg'   
    )
    
    login_button = InlineKeyboardButton(
        text='🔑 Войти в аккаунт',
        callback_data='login'
    )
    # Добавляем кнопки в клавиатуру 
    keyboard: list[list[InlineKeyboardButton]] = [
        [start_reg_button],
        [login_button]
    ]
    # Создаем объект инлайн-клавиатуры
    menu_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu_markup


# кнопки для регистрации пользователя
def menu_reg_start():
    start_reg_button = InlineKeyboardButton(
        text='✅ Зарегестрироваться',
        callback_data='start_reg'   
    )
    
    # Добавляем кнопки в клавиатуру 
    keyboard: list[list[InlineKeyboardButton]] = [
        [start_reg_button],
    ]
    # Создаем объект инлайн-клавиатуры
    menu_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu_markup




