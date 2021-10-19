"""
[+] пользак выбирает категорию из предложенных и вписывает руками сумму, дату, описание
[+] бот вписывает расход в нужное место пока хватит
[+] последние 10 ваших расходов, сумма всех внесенных расходов
[+] кнопки в нижней клавиатуре работают или очищаются инлайновые (сделал очистку, кнопки внизу командные)
[-] календарь кнопками
"""

import telebot
from telebot import types
import datetime
import csv
import mytoken
# import telegramcalendar

bot = telebot.TeleBot(f"{mytoken.token}")
markup = types.ReplyKeyboardMarkup(row_width=1)


@bot.message_handler(commands=['b'])
def main_menu(message):
	markup = types.ReplyKeyboardMarkup(row_width=1)
	itembtn1 = types.KeyboardButton('Добавить расход')
	itembtn2 = types.KeyboardButton('Сумма всех расходов')
	itembtn3 = types.KeyboardButton('Последние 5 записей')
	markup.add(itembtn1, itembtn2, itembtn3)
	bot.send_message(message.from_user.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def add_entry(message):
	test1 = message.chat.id
	test2 = message.id
	if message.text == 'Добавить расход':
		markup_delete = types.ReplyKeyboardRemove()
		bot.send_message(message.from_user.id, "=== Добавить расход ===", reply_markup=markup_delete)
		bot.delete_message(message.chat.id, message.id - 2)
		bot.delete_message(message.chat.id, message.id - 1)
		bot.delete_message(message.chat.id, message.id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard_1 = types.InlineKeyboardButton(text='продукты', callback_data=f'{test1}+{test2}+test1')
		keyboard.add(keyboard_1)
		keyboard_2 = types.InlineKeyboardButton(text='тачка', callback_data=f'{test1}+{test2}+test2')
		keyboard.add(keyboard_2)
		keyboard_3 = types.InlineKeyboardButton(text='пиво', callback_data='beer')
		keyboard.add(keyboard_3)
		bot.send_message(message.from_user.id, text='Выберите категорию:', reply_markup=keyboard)
	elif message.text == 'Сумма всех расходов':
		summ_all(message)
	elif message.text == 'Последние 5 записей':
		last(message)
	else:
		print('неизвестная команда')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	command = call.data.split('+')[2]
	test1 = call.data.split('+')[0]
	test2 = call.data.split('+')[1]
	if command == "test1":
		bot.delete_message(chat_id=test1, message_id=int(test2) + 2)
		# bot.delete_message(chat_id=test1, message_id=int(test2) + 1)
		cat = 'продукты'
		# markup1 = types.ReplyKeyboardRemove(selective=False)
		# bot.send_message(call.message.chat.id, 'кнопки удалены', reply_markup=markup1)
		bot.register_next_step_handler(bot.send_message(call.message.chat.id, 'введи сумму (c для отмены):'),
									   _sum, cat)
	if call.data == "test2":
		bot.delete_message(chat_id=test1, message_id=test2)
		bot.delete_message(chat_id=test1, message_id=int(test2) + 1)
		cat = 'тачка'
		# markup1 = types.ReplyKeyboardRemove(selective=False)
		# bot.send_message(call.message.chat.id, 'кнопки удалены', reply_markup=markup1)
		bot.register_next_step_handler(bot.send_message(call.message.chat.id, 'введи сумму (c для отмены):'),
									   _sum, cat)
	if call.data == "beer":
		bot.delete_message(chat_id=test1, message_id=test2)
		bot.delete_message(chat_id=test1, message_id=int(test2) + 1)
		bot.send_message(call.message.chat.id, 'а вот это отлично')


def _sum(message, cat):
	if message.text.lower() == 'c' or message.text.lower() == 'с':
		main_menu(message)
	else:
		bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
		bot.delete_message(chat_id=message.chat.id, message_id=message.id)
		new_entry = []
		bot.send_message(message.from_user.id, text=f'сумма = {message.text}')
		new_entry.append(cat)
		new_entry.append(message.text)
		bot.register_next_step_handler(bot.send_message(message.chat.id, 'введи название (c для отмены)'),
									   name, new_entry)


def name(message, new_entry):
	if message.text.lower() == 'c' or message.text.lower() == 'с':
		main_menu(message)
	else:
		bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
		bot.delete_message(chat_id=message.chat.id, message_id=message.id)
		bot.send_message(message.from_user.id, text=f'название = {message.text}')
		new_entry.append(message.text)
		bot.register_next_step_handler(bot.send_message(message.chat.id, 'выбери дату (c для отмены)'),
									   _date, new_entry)


def _date(message, new_entry):
	if message.text.lower() == 'c' or message.text.lower() == 'с':
		main_menu(message)
	else:
		bot.delete_message(chat_id=message.chat.id, message_id=message.id - 5)
		bot.delete_message(chat_id=message.chat.id, message_id=message.id - 2)
		bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
		bot.delete_message(chat_id=message.chat.id, message_id=message.id)
		convert_date = datetime.datetime.strptime(message.text, '%d.%m.%Y').isoformat(sep='T')
		new_entry.append(convert_date)
		# bot.send_message(message.from_user.id, text=f'дата datetime = {convert_date}')
		bot.send_message(message.from_user.id, text=f'внесён расход = {new_entry}')
		main_menu(message)
		with open("finances.csv", mode="a", encoding='utf-8') as w_file:
			file_writer = csv.writer(w_file, lineterminator="\r")
			file_writer.writerow(new_entry)


# @bot.message_handler(commands=['c'])
# def cancel(message):
# 	add_entry(message)


# @bot.message_handler(content_types=['text'])
def summ_all(message):
	summ = 0
	with open("finances.csv", mode="r", encoding='utf-8') as r_file:
		file_reader = csv.reader(r_file, lineterminator="\r")
		for row in file_reader:
			summ += int(row[1])
	bot.send_message(message.from_user.id, text=f'Сумма всех расходов = {summ}')


# @bot.message_handler(content_types=['text'])
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
			if j >= i - 4:  # здесь регулируется кол-во последних записей
				last += str(row)
	bot.send_message(message.from_user.id, text=f'{last}')


bot.infinity_polling()
