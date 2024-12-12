""" 
Модуль представляет собой набор функций для управления базой данных SQLite, используемой ботом. 
Основные задачи этого модуля включают создание таблиц, запись и извлечение данных о пользователях, 
их образовательных предметах и сообщениях, отправленных боту.

### Основные функции модуля:
1. db_start():
   - Устанавливает соединение с базой данных db_bota.db.
   - Создает курсор для выполнения SQL-запросов.
   - Проверяет наличие и создает три таблицы:
     - profile: содержит информацию о зарегистрированных пользователях (ID, имя, фамилия).
     - educational_subjects: содержит данные об учебных предметах и набранных баллах пользователями.
     - message_from_users: сохраняет сообщения от пользователей вместе с датой отправки.

2. create_profile(date_profile, user_id):
   - Добавляет нового пользователя в таблицу profile, используя переданные параметры (user_id, first_name, last_name).

3. load_user(user_id):
   - Извлекает данные пользователя по его ID из таблицы profile и возвращает их в виде списка.

4. update_educational_subjects(data_subject, user_id):
   - Обновляет или добавляет информацию о предмете и баллах пользователя в таблице educational_subjects.

5. load_educational_subjects(user_id):
   - Загружает данные об учебных предметах и баллах конкретного пользователя из таблицы educational_subjects и возвращает их в виде списка.

6. update_message(message, user_id):
   - Сохраняет сообщение от пользователя в таблицу message_from_users вместе с текущей датой.
"""

import sqlite3 as sq
from datetime import date

# Запуск базы данных 
async def db_start():
    global db, cur
    
    # создем экземпляр базы даных с названием файла, где она будет храниться
    db = sq.connect('db_bota.db')
    cur = db.cursor()
    
    # Создаем таблицу данных пользователей 
    cur.execute('CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT)')
    
    # Создаем таблицу данных по предметам ЕГЭ и баллам
    cur.execute('CREATE TABLE IF NOT EXISTS educational_subjects(user_id TEXT, name_subject TEXT, points_subject INTEGER)')
    
    # Создаем таблицу данных по написанным боту сообщениям для обработки, что не покрывает основной функционал
    cur.execute('CREATE TABLE IF NOT EXISTS message_from_users(user_id TEXT, message TEXT, day TEXT)')
    
    db.commit()

     
# Заполнение таблицы profile после регистрации пользвателя с сохранением его данных
async def create_profile(date_profile, user_id):
    cur.execute("INSERT INTO profile VALUES('{}', '{}', '{}')".format(user_id, 
                date_profile['first_name'], date_profile['last_name']))
   
    db.commit()


# Выгрузка данных пользователя из базы данных
async def load_user(user_id):
    # выгружаем данные пользователя по id
    load_user_bd = cur.execute("SELECT * FROM profile WHERE user_id == '{}' ".format(user_id)).fetchall()
    
    loads = [] # возвращаем данные из БД в виде списка
    for user in load_user_bd:
        loads.append(user)
    db.commit()
    return loads
    

# Заполнение таблицы educational_subjects после отправки боту данных по предмету
async def create_educational_subjects(data_subject, user_id):
    cur.execute("INSERT INTO educational_subjects VALUES('{}', '{}', '{}')".format(user_id, 
                data_subject['name_subject'], data_subject['points_subject']))
    db.commit()


# Выгрузка данных по предмета по id пользователя
async def load_educational_subjects(user_id):
    load_educational_subjects_bd = cur.execute("SELECT * FROM educational_subjects WHERE user_id == '{}' ".format(user_id)).fetchall()
    
    loads = [] # возвращаем данные из БД в виде списка
    for educational in load_educational_subjects_bd:
        loads.append(educational)
    db.commit()
    return loads
 
    
# Заполнение таблицы message_from_users после отправки боту сообщения
async def create_message(message, user_id):
    today = date.today().strftime("%d.%m.%Y")     # создаем переменню и записываем дату сообщения
    cur.execute("INSERT INTO message_from_users VALUES('{}', '{}', '{}')".format(user_id, message, today))
    db.commit()
    