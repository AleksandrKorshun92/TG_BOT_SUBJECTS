""" 
Этот модуль представляет собой реализацию фильтра для проверки статуса регистрации пользователей 
в системе. Фильтр предназначен для предотвращения повторной регистрации уже зарегистрированных пользователей.

Основные компоненты модуля:
1. Класс RegistrationFilter:
   - Наследуется от базового класса фильтров BaseFilter.
   - Содержит метод call, который выполняет основную логику работы фильтра.

2. Метод call:
   - Принимает событие (сообщение или коллбек), связанное с пользователем.
   - Загружает информацию о пользователе из базы данных через функцию load_user.
   - Проверяет, зарегистрирован ли пользователь в системе.
   - Если пользователь уже зарегистрирован, отправляет ему сообщение о том, что регистрация невозможна, и возвращает False, чтобы заблокировать дальнейшую обработку.
   - Если пользователь не зарегистрирован, возвращает True, позволяя продолжить процесс регистрации.

"""

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from lexicon.lexicon import LEXICON
from database.sqlite3 import load_user


class RegistrationFilter(BaseFilter):
    """Фильтр для проверки статуса регистрации пользователя.
    Attributes:
        None

    Methods:
        call(event: Union[Message, CallbackQuery]) -> bool:
            Метод вызова фильтра. Проверяет статус регистрации пользователя и возвращает результат.

    Raises:
        TypeError: Если тип события не является ни Message, ни CallbackQuery.
    """
    
    async def __call__(self, event):
        user_id = event.from_user.id
        # Загружаем из базы данных по пользователю по id
        user_sql = await load_user(user_id=user_id)
        
        # Проверяем статус регистрации
        registration_status = True if user_sql else False
        
        if registration_status:
            # Если пользователь уже зарегистрирован, блокируем регистрацию
            if isinstance(event, CallbackQuery):
                await event.message.answer(text=LEXICON['start_message'])
            else:
                await event.answer(text=LEXICON['start_message'])
            return  False
            
        else:
            return True 





