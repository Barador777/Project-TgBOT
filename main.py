import dateparser
import telebot
from telebot import types
import sqlite3
import re
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from datetime import datetime

bot = telebot.TeleBot('')
scheduler = BackgroundScheduler()
scheduler.start()

def init_db():
    conn = sqlite3.connect('reminders.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reminders
                      (user_id INTEGER,
                        type TEXT,
                        content TEXT,
                        time TEXT)''')
    conn.commit()
    conn.close()

init_db()

def send_reminder(user_id, text, r_type):
    bot.send_message(user_id, f"{r_type.upper()}: {text}")
    if r_type == 'Одноразовое':
        conn = sqlite3.connect('reminders.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reminders WHERE user_id = ? AND content LIKE ?", (user_id, f"%{text}%"))
        conn.commit()
        conn.close()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1, btn2, btn3 = types.KeyboardButton('Сделать напоминание'), types.KeyboardButton(
        'Все записи напоминаний'), types.KeyboardButton('О боте')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Привет! 🤗 Я ваш персональный бот помошник, готов поставить любое ваше напоминание!', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.lower()
    if text == 'сделать напоминание':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add('Ежедневное', 'Каждый год', 'Одноразовое', 'Назад')
        bot.send_message(message.chat.id, 'Выберите тип напоминания:', reply_markup=markup)
    elif text in ['ежедневное', 'каждый год', 'одноразовое']:
        msg = bot.send_message(message.chat.id, f'Введите текст и время для типа "{text}".\nНапример: купить водку 13 февраля в 10:40 или выпить лекарство в 9:00')
        bot.register_next_step_handler(msg, save_and_schedule, text.capitalize())
    elif text == 'все записи напоминаний':
        show_reminders(message)
    elif text == 'назад':
        start(message)
    elif text == 'о боте':
        bot.send_message(message.from_user.id, 'Этот бот - ваш удобный и надёжный помощник для создания и управления напоминаниями. \n' +
'С его помощью вы легко сможете:\n' +
'· Добавлять напоминания о важных делах, встречах и событиях;\n' +
'· Получать уведомления в нужное время, чтобы ничего не забыть;\n' +
'· Настраивать регулярные повторяющиеся напоминания;\n' +
'· Управлять списком задач через простой интерфейс.\n' +
'Идеально подходит для планирования дня, учёбы, работы и личных дел.\n' +
'Бот работает 24/7 и всегда напомнит вовремя!\n' +
'Простота, удобство и эффективность — сделайте планирование лёгким с нашим ботом.', parse_mode='Markdown')

def show_reminders(message):
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT type, content, time FROM reminders WHERE user_id = ?", (message.chat.id,))
    rows = cursor.fetchall()
    conn.close()
    if rows:
        res = "Ваши записи:\n\n" + "\n".join([f"· ({r[0]}) {r[1]}" for r in rows])
        bot.send_message(message.chat.id, res)
    else:
        bot.send_message(message.chat.id, 'Список пуст 😞')


def save_and_schedule(message, r_type):
    user_id = message.chat.id
    user_text = message.text

    parsed_date = dateparser.parse(user_text, settings={'PREFER_DATES_FROM': 'future', 'DATE_ORDER': 'DMY'})

    if not parsed_date:
        clean_match = re.search(r'(\d{1,2}\s+[а-яА-Я]+\s+в\s+\d{1,2}:\d{2})|(\d{1,2}:\d{2})|(\d{1,2}\.\d{1,2})',
                                user_text)
        if clean_match:
            parsed_date = dateparser.parse(clean_match.group(),
                                           settings={'PREFER_DATES_FROM': 'future', 'DATE_ORDER': 'DMY'})

    if parsed_date:
        parsed_date = parsed_date.replace(second=0, microsecond=0)

        parsed_date = parsed_date.replace(second=0, microsecond=0)
        rem_time = parsed_date.strftime("%H:%M")
        rem_date_str = parsed_date.strftime("%d.%m.%Y")

        conn = sqlite3.connect('reminders.db')
        cursor = conn.cursor()
        full_content = f"{user_text} (на {rem_date_str})"
        cursor.execute("INSERT INTO reminders VALUES (?, ?, ?, ?)",
                       (user_id, r_type, full_content, rem_time))
        conn.commit()
        conn.close()

        if r_type == 'Ежедневное':
            scheduler.add_job(send_reminder, 'cron', hour=parsed_date.hour, minute=parsed_date.minute,
                              args=[user_id, user_text, r_type])
            bot.send_message(user_id, f"Ежедневно в {rem_time}")

        elif r_type == 'Каждый год':
            scheduler.add_job(send_reminder, 'cron', month=parsed_date.month, day=parsed_date.day,
                              hour=parsed_date.hour, minute=parsed_date.minute, args=[user_id, user_text, r_type])
            bot.send_message(user_id, f"Каждый год {parsed_date.day:02d}.{parsed_date.month:02d} в {rem_time}")

        else:
            scheduler.add_job(send_reminder, 'date', run_date=parsed_date,
                              args=[user_id, user_text, r_type])
            bot.send_message(user_id, f"Напомню {rem_date_str} в {rem_time}")

        start(message)
    else:
        bot.send_message(user_id, "Не удалось распознать дату или время.\n\nПопробуй написать точнее, например:\n— 'Завтра в 15:00'\n— '25 мая в 10:30'\n— 'Через 2 часа'")


def restore_jobs():
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, type, content, time FROM reminders")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        user_id, r_type, content, rem_time = row
        h, m = map(int, rem_time.split(':'))

        if r_type == 'Ежедневное':
            scheduler.add_job(send_reminder, 'cron', hour=h, minute=m, args=[user_id, content, r_type])
        elif r_type == 'Каждый год':
            scheduler.add_job(send_reminder, 'cron', month='*', day='*', hour=h, minute=m, args=[user_id, content, r_type])
        elif r_type == 'Одноразовое':
            scheduler.add_job(send_reminder, 'cron', hour=h, minute=m, args=[user_id, content, r_type])

restore_jobs()
bot.polling(none_stop=True)
