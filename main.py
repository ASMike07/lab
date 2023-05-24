import datetime
import os

import timetable as timetable
import psycopg2
import telebot
from telebot import types

# Коннект с базой данных
conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="deadmike07",
    database="inform"
)

BOT_TOKEN = "5924128243:AAFY_ZQ9vhR2110MUmlAVylM20plJRaHW60"

# Инициализация бота с помощью токена
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    # Создание встроенной клавиатуры
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    monday_button = types.InlineKeyboardButton(text="Понедельник", callback_data="Monday")
    tuesday_button = types.InlineKeyboardButton(text="Вторник", callback_data="Tuesday")
    wednesday_button = types.InlineKeyboardButton(text="Среда", callback_data="Wednesday")
    thursday_button = types.InlineKeyboardButton(text="Четверг", callback_data="Thursday")
    friday_button = types.InlineKeyboardButton(text="Пятница", callback_data="Friday")
    keyboard.add(monday_button, tuesday_button, wednesday_button, thursday_button, friday_button)

    # Отправка приветственного сообщения с встроенной клавиатурой
    bot.reply_to(message, "Добро пожаловать! Выберите день недели:", reply_markup=keyboard)

# Определение команды /week
@bot.message_handler(commands=['week'])
def week_command(message):
    # Получить номер текущей недели
    week_number = datetime.datetime.now().isocalendar()[1]
    # Определить верхнюю/нижнюю неделю
    if week_number % 2 == 0:
        week_type = "верхняя"
    else:
        week_type = "нижняя"
    # Отправить пользователю информацию о неделе
    bot.send_message(message.chat.id, f"Текущая неделя: {week_type} (Неделя года: {week_number})")

# Определение команды /mtuci
@bot.message_handler(commands=['mtuci'])
def mtuci_command(message):
    # Отправить пользователю ссылку на веб-сайт МТУСИ
    bot.send_message(message.chat.id, "Вот ссылка на официальный сайт MTUCI: https://mtuci.ru")


# Определите команду /help
@bot.message_handler(commands=['help'])
def help_command(message):
    # Отправка пользователю информации о боте и списока команд
    bot.send_message(message.chat.id, "Я бот, который может помочь Вам получить информацию о расписании группы БВТ2207 МТУСИ!\n\nВот команды, которые я понимаю:\n\n/week - Получить информацию о текущей неделе (верхняя/нижняя)\n/mtuci - Получить ссылку на официальный веб-сайт МТУСИ\n/help - Получить список команд")

# Определите обработчик сообщений для неизвестных команд или сообщений
@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    # Отправьте сообщение с извинениями пользователю за то, что он не понял их сообщения
    bot.send_message(message.chat.id, "Извините, я Вас не понял")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    week_number = datetime.datetime.now().isocalendar()[1]
    if call.data == 'Monday':
        cur = conn.cursor()
        cur.execute("SELECT * FROM schedule WHERE day_of_week = 'Понедельник' AND week = %s", [week_number])
        rows = cur.fetchall()
        cur.close()
        schedule_text = "Расписание на понедельник (Неделя {}):\n".format(week_number)
        for row in rows:
            schedule_text += "Предмет: {}\nВремя начала: {}\nВремя окончания: {}\n\n".format(row[2], row[3], row[4])
        bot.send_message(call.message.chat.id, schedule_text)
    elif call.data == 'Tuesday':
        cur = conn.cursor()
        cur.execute("SELECT * FROM schedule WHERE day_of_week = 'Вторник' AND week = %s", [week_number])
        rows = cur.fetchall()
        cur.close()
        schedule_text = "Расписание на вторник (Неделя {}):\n".format(week_number)
        for row in rows:
            schedule_text += "Предмет: {}\nВремя начала: {}\nВремя окончания: {}\n\n".format(row[2], row[3], row[4])
        bot.send_message(call.message.chat.id, schedule_text)
    elif call.data == 'Wednesday':
        cur = conn.cursor()
        cur.execute("SELECT * FROM schedule WHERE day_of_week = 'Среда' AND week = %s", [week_number])
        rows = cur.fetchall()
        cur.close()
        schedule_text = "Расписание на среду (Неделя {}):\n".format(week_number)
        for row in rows:
            schedule_text += "Предмет: {}\nВремя начала: {}\nВремя окончания: {}\n\n".format(row[2], row[3], row[4])
        bot.send_message(call.message.chat.id, schedule_text)
    elif call.data == 'Thursday':
        cur = conn.cursor()
        cur.execute("SELECT * FROM schedule WHERE day_of_week = 'Четверг' AND week = %s", [week_number])
        rows = cur.fetchall()
        cur.close()
        schedule_text = "Расписание на четверг (Неделя {}):\n".format(week_number)
        for row in rows:
            schedule_text += "Предмет: {}\nВремя начала: {}\nВремя окончания: {}\n\n".format(row[2], row[3], row[4])
        bot.send_message(call.message.chat.id, schedule_text)
    elif call.data == 'Friday':
        cur = conn.cursor()
        cur.execute("SELECT * FROM schedule WHERE day_of_week = 'Пятница' AND week = '{}'".format(week_number))
        print(cur.execute)
        rows = cur.fetchall()
        #Расписание на пятницу (Неделя 20):
        cur.close()
        schedule_text = "Расписание на пятницу (Неделя {}):\n".format(week_number)
        for row in rows:
            schedule_text += "Предмет: {}\nВремя начала: {}\nВремя окончания: {}\n\n".format(row[2], row[3], row[4])
        bot.send_message(call.message.chat.id, schedule_text)
    elif call.data == 'CurrentWeek':
        cur = conn.cursor()
        cur.execute("SELECT * FROM schedule WHERE week = %s", (week_number),)
        rows = cur.fetchall()
        cur.close()
        schedule_text = "Расписание на текущую неделю (Неделя {}):\n".format(week_number)
        for row in rows:
            schedule_text += "День недели: {}\nПредмет: {}\nВремя начала: {}\nВремя окончания: {}\n\n".format(row[1], row[2], row[3], row[4])
        bot.send_message(call.message.chat.id, schedule_text)


# Определите обработчик запроса обратного вызова для встроенных кнопок клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_callback(call):
    # Получить выбранный день недели из callback data
    day_of_week = call.data
    # Определение запроса PostgreSQL на основе выбранного дня недели
    if day_of_week == "current_week":
        query = f"SELECT * FROM schedule WHERE week_number = {datetime.datetime.now().isocalendar()[1]}"
    else:
        query = f"SELECT * FROM schedule WHERE day_of_week = '{day_of_week}' AND week_number = {datetime.datetime.now().isocalendar()[1]}"
    # Выполнение запроса и получение результатов
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    # Отправка информации о расписании пользователю
    if len(rows) == 0:
        bot.answer_callback_query(call.id, " Не найдено занятий для выбранного дня/недели")
    else:
        schedule_text = ""
        for row in rows:
            schedule_text += f"{row[1]} - {row[2]} ({row[3]} - {row[4]})\n"
        bot.send_message(call.message.chat.id, schedule_text)

# Определение основного обработчика для команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    # Отправка пользователю приветственного сообщения и встроенной клавиатуры с указанием дней недели
    bot.send_message(message.chat.id, "Добро пожаловать в бот расписания МТУСИ!", reply_markup=days_keyboard)


# Запуск бота
bot.polling()

