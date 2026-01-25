import telebot
from telebot import types

bot = telebot.TeleBot('')

@bot.message_handler(commands=['start'])
def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Кнопка 1')
        btn2 = types.KeyboardButton('Связь с разработчиком')
        btn3 = types.KeyboardButton('Кнопка 3')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, 'Задайте интересующий вас вопрос', reply_markup=markup)

@bot.message_handler(content_types=['text']) #действия бота
def handle_text(message):
        text = message.text.lower()

        if text == 'кнопка 1':
            bot.send_message(message.from_user.id, '12345 ' + '[ссылка](https://github.com/Barador777?tab=repositories)', parse_mode='Markdown')

        elif text == 'связь с разработчиком':
            bot.send_message(message.from_user.id, 'Автор проекта:' + ' @Tarantagg', parse_mode='Markdown')

        elif text == 'кнопка 3':
            bot.send_message(message.from_user.id, '6789 ' + '[ссылка](https://github.com/Barador777?tab=repositories)', parse_mode='Markdown')


bot.polling(none_stop=True, interval=0)