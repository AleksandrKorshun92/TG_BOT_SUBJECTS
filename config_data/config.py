"""Модуль для загрузки конфигурации Telegram-бота из переменных окружения.
Использует библиотеку environs для чтения значений из .env файла.

Пример использования:
config = load_config('.env')
Где `.env` файл может содержать: BOT_TOKEN=1234567890:AbCdEfGhIjKlMnOpQrStUvWxYz0123456789

В результате будет создан объект типа Config, содержащий экземпляр TgBot с токеном.
"""


from dataclasses import dataclass
from environs import Env 

@dataclass
class TgBot():
    token: str 

@dataclass
class Config:
    tg_bot: TgBot 


# создания экземпляра телеграмм бота
def load_config(path = None) -> Config:
    """
    Функция для загрузки конфигурации из переменных окружения.

    Аргументы:
        path (str | None): Путь к файлу .env. Если не указан, используется текущий рабочий каталог.

    Возвращает:
        Config: Объект типа Config, содержащий загруженную конфигурацию.
    """
    env = Env()
    env.read_env(path) # путь для файла env где хранится токен
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))

