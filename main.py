"""
[+] пользак выбирает категорию из предложенных и вписывает руками сумму, дату, описание
[+] бот вписывает расход в нужное место пока хватит
[-] последние 10 ваших расходов, сумма всех внесенных расходов
"""

import telebot
from telebot import types
import datetime
import csv
import mytoken

bot = telebot.TeleBot(f"{mytoken.token}")
status_message = 0


def test():
	print('функция сработала')


@bot.message_handler(commands=['s'])
def main_menu(message):
	keyboard = types.InlineKeyboardMarkup()
	keyboard_1 = types.InlineKeyboardButton(text='продукты', callback_data='test1')
	keyboard.add(keyboard_1)
	keyboard_2 = types.InlineKeyboardButton(text='тачка', callback_data='test2')
	keyboard.add(keyboard_2)
	keyboard_3 = types.InlineKeyboardButton(text='пиво', callback_data='beer')
	keyboard.add(keyboard_3)
	bot.send_message(message.from_user.id, text='Выбери категорию', reply_markup=keyboard)


@bot.message_handler(commands=['sum'])
def summ_all(message):
	summ = 0
	with open("finances.csv", mode="r", encoding='utf-8') as r_file:
		file_reader = csv.reader(r_file, lineterminator="\r")
		for row in file_reader:
			summ += int(row[1])
	bot.send_message(message.from_user.id, text=f'Сумма всех расходов = {summ}')


@bot.message_handler(commands=['last'])
def last(message):
	last = ''
	i = 0
	with open("finances.csv", mode="r", encoding='utf-8') as r_file:
		file_reader = csv.reader(r_file, lineterminator="\r")
		for row in file_reader:
			i += 1

	with open("finances.csv", mode="r", encoding='utf-8') as r_file:
		file_reader = csv.reader(r_file, lineterminator="\r")
		j = 0
		for row in file_reader:
			j += 1
			if j >= i - 1:
				last += str(row)
	bot.send_message(message.from_user.id, text=f'{last}')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if call.data == "test1":
		cat = 'продукты'
		bot.register_next_step_handler(bot.send_message(call.message.chat.id, 'введи сумму:'), _sum, cat)
	if call.data == "test2":
		cat = 'тачка'
		bot.register_next_step_handler(bot.send_message(call.message.chat.id, 'введи сумму:'), _sum, cat)
	if call.data == "beer":
		bot.send_message(call.message.chat.id, 'а вот это отлично')


def _sum(message, cat):
	new_entry = []
	bot.send_message(message.from_user.id, text=f'сумма = {message.text}')
	new_entry.append(cat)
	new_entry.append(message.text)
	bot.register_next_step_handler(bot.send_message(message.chat.id, 'введи название'), name, new_entry)


def name(message, new_entry):
	bot.send_message(message.from_user.id, text=f'название = {message.text}')
	new_entry.append(message.text)
	bot.register_next_step_handler(bot.send_message(message.chat.id, 'выбери дату'), _date, new_entry)


def _date(message, new_entry):
	convert_date = datetime.datetime.strptime(message.text, '%d.%m.%Y').isoformat(sep='T')
	new_entry.append(convert_date)
	bot.send_message(message.from_user.id, text=f'дата datetime = {convert_date}')
	with open("finances.csv", mode="a", encoding='utf-8') as w_file:
		file_writer = csv.writer(w_file, lineterminator="\r")
		file_writer.writerow(new_entry)


bot.infinity_polling()
