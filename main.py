'''
пользак выбирает категорию из предложенных и вписывает руками сумму, дату, описание
бот вписывает расход в нужное место пока хватит
'''

import telebot
from telebot import types

bot = telebot.TeleBot("2041146411:AAGW4K_Dnii5xb6Q9tnxSexk_9kFc_LofPQ")


def test():
	print('функция сработала')


@bot.message_handler(commands=['s'])
def main_menu(message):
	keyboard = types.InlineKeyboardMarkup()
	keyboard_1 = types.InlineKeyboardButton(text='продукты', callback_data='test')
	keyboard.add(keyboard_1)
	keyboard_2 = types.InlineKeyboardButton(text='тачка', callback_data='test')
	keyboard.add(keyboard_2)
	keyboard_3 = types.InlineKeyboardButton(text='пиво', callback_data='beer')
	keyboard.add(keyboard_3)
	bot.send_message(message.from_user.id, text='Выбери категорию', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if call.data == "test":
		bot.send_message(call.message.chat.id, 'введи сумму:')
	if call.data == "beer":
		bot.send_message(call.message.chat.id, 'а вот это отлично')


@bot.message_handler()
def answer(message):
	bot.send_message(message.from_user.id, text=f'сумма = {message.text}')


bot.infinity_polling()
