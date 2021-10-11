import telebot
from telebot import types

bot = telebot.TeleBot("")


@bot.message_handler(commands=['start'])
def eee(message):
	chat_id = message.chat.id
	markup = types.ReplyKeyboardMarkup()
	itembtn_1 = types.KeyboardButton('категория1')
	itembtn_2 = types.KeyboardButton('категория2')
	itembtn_3 = types.KeyboardButton('категория3')
	itembtn_4 = types.KeyboardButton('категория4')
	itembtn_5 = types.KeyboardButton('категория5')
	itembtn_6 = types.KeyboardButton('категория6')
	markup.row(itembtn_1, itembtn_2)
	markup.row(itembtn_3, itembtn_4)
	markup.row(itembtn_5, itembtn_6)
	bot.send_message(chat_id, "выбери категорию:", reply_markup=markup)


bot.infinity_polling()
