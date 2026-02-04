import telebot
from telebot import types

bot = telebot.TeleBot('')

@bot.message_handler(commands=['start'])
def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Сделать напоминание')
        btn2 = types.KeyboardButton('Все записи напоминаний')
        btn3 = types.KeyboardButton('О боте')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, 'Привет! 🤗 Я ваш персональный бот помошник, готов поставить любое ваше напоминание!', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
        text = message.text.lower()

        if text == 'сделать напоминание':
            reminder_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton('Ежедневное')
            btn2 = types.KeyboardButton('Каждый год')
            btn3 = types.KeyboardButton('Одноразовое')
            btn4 = types.KeyboardButton('Назад')
            reminder_markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.from_user.id, 'Выберите тип напоминания:', reply_markup=reminder_markup)

        elif text == 'все записи напоминаний':
            bot.send_message(message.from_user.id, 'Эта функция пока недоступна')

        elif text == 'о боте':
            bot.send_message(message.from_user.id, 'Этот бот — ваш удобный и надёжный помощник для создания и управления напоминаниями. ' +
'С его помощью вы легко сможете:\n' +
'· Добавлять напоминания о важных делах, встречах и событиях;\n' +
'· Получать уведомления в нужное время, чтобы ничего не забыть;\n' +
'· Настраивать регулярные повторяющиеся напоминания;\n' +
'· Управлять списком задач через простой интерфейс.\n' +
'Идеально подходит для планирования дня, учёбы, работы и личных дел.\n' +
'Бот работает 24/7 и всегда напомнит вовремя!\n' +
'Простота, удобство и эффективность — сделайте планирование лёгким с нашим ботом.', parse_mode='Markdown')

        elif text == 'назад':
            # Возвращаемся к главной клавиатуре
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Сделать напоминание')
            btn2 = types.KeyboardButton('Все записи напоминаний')
            btn3 = types.KeyboardButton('О боте')
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, 'Привет!🤗 Я ваш персональный бот помошник, готов поставить любое ваше напоминание!', reply_markup=markup)

        elif text == 'ежедневное':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Назад')
            markup.add(btn1)
            bot.send_message(message.from_user.id, 'Напишите пожалуйста время и напоминание в одном сообщении.\nНапример: Выпить лекарство в 7:30', reply_markup=markup)

        elif text == 'каждый год':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Назад')
            markup.add(btn1)
            bot.send_message(message.from_user.id, 'Напишите пожалуйста время и напоминание в одном сообщении.\nНапример: Поздравить с ДР Алексея 15 мая в 9:30', reply_markup=markup)

        elif text == 'одноразовое':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Назад')
            markup.add(btn1)
            bot.send_message(message.from_user.id, 'Напишите пожалуйста время и напоминание в одном сообщении.\nНапример: Купить хлеб завтра в 12:00', reply_markup=markup)

bot.polling(none_stop=True, interval=0)
