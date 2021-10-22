"""
[+] пользак выбирает категорию из предложенных и вписывает руками сумму, дату, описание
[+] бот вписывает расход в нужное место пока хватит
[+] последние 10 ваших расходов, сумма всех внесенных расходов
[+] кнопки в нижней клавиатуре работают или очищаются инлайновые (сделал очистку, кнопки внизу командные)
[+] календарь кнопками
"""

import telebot
from telebot import types
import datetime
import csv
import mytoken
import calendar

bot = telebot.TeleBot(f"{mytoken.token}")
# chat_id = mytoken.my_chat_id
chat_id = 0
global_month = 0
global_year = 0
calendar_message_id = 0
category_message = 0
new_entry = []


@bot.message_handler(commands=['start'])
def start_bot(message):
    global chat_id
    chat_id = message.chat.id
    main_menu()


def show_calendar(message):
    global message_id
    message_id = message.id + 1
    now_month = datetime.datetime.now().month
    now_year = datetime.datetime.now().year
    bot.send_message(chat_id, 'Выберите дату:', reply_markup=inline_calendar(now_year, now_month))


def change_calendar(current_year, current_month):
    global message_id
    bot.edit_message_text(text='Выберите дату:', chat_id=chat_id, message_id=message_id,
                          reply_markup=inline_calendar(current_year, current_month))


def inline_calendar(year, month):
    calendar_buttons = types.InlineKeyboardMarkup(row_width=7)
    month_btn = types.InlineKeyboardButton(f'{month}', callback_data='asda')
    calendar_buttons.row(month_btn)
    for i in calendar.monthcalendar(year, month):
        rr = []
        for day in i:
            btn = types.InlineKeyboardButton(f'{day}', callback_data=f'certain_date+{day}+{month}+{year}')
            rr.append(btn)
        calendar_buttons.row(rr[0], rr[1], rr[2], rr[3], rr[4], rr[5], rr[6])
    back_btn = types.InlineKeyboardButton('<', callback_data='back_month')
    forward_btn = types.InlineKeyboardButton('>', callback_data='forward_month')
    calendar_buttons.row(back_btn, forward_btn)
    global global_year, global_month
    global_year = year
    global_month = month
    return calendar_buttons


@bot.message_handler(commands=['b'])
def main_menu(*args):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Добавить расход')
    itembtn2 = types.KeyboardButton('Сумма всех расходов')
    itembtn3 = types.KeyboardButton('Последние 5 записей')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def add_entry(message):
    if message.text == 'Добавить расход':
        markup_delete = types.ReplyKeyboardRemove()
        bot.send_message(chat_id, "=== Добавить расход ===", reply_markup=markup_delete)
        keyboard = types.InlineKeyboardMarkup()
        keyboard_1 = types.InlineKeyboardButton(text='Продукты', callback_data=f'category+Продукты')
        keyboard.add(keyboard_1)
        keyboard_2 = types.InlineKeyboardButton(text='Тачка', callback_data=f'category+Тачка')
        keyboard.add(keyboard_2)
        keyboard_3 = types.InlineKeyboardButton(text='Пиво', callback_data=f'category+Пиво')
        keyboard.add(keyboard_3)
        bot.send_message(chat_id, text='Выберите категорию:', reply_markup=keyboard)
        global category_message
        category_message = message.id + 2
    elif message.text == 'Сумма всех расходов':
        summ_all()
    elif message.text == 'Последние 5 записей':
        last()
    else:
        bot.send_message(message.from_user.id, text='Неизвестная команда')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    command = call.data.split('+')[0]

    global global_year, global_month
    if call.data == 'back_month':
        if global_month == 1:
            global_year -= 1
            global_month = 12
            change_calendar(global_year, global_month)
        else:
            global_month -= 1
            change_calendar(global_year, global_month)
    if call.data == 'forward_month':
        if global_month == 12:
            global_year += 1
            global_month = 1
            change_calendar(global_year, global_month)
        else:
            global_month += 1
            change_calendar(global_year, global_month)

    if call.data.split('+')[0] == 'certain_date':
        global new_entry
        day = call.data.split('+')[1]
        month = call.data.split('+')[2]
        year = call.data.split('+')[3]
        convert_date = f'{day}.{month}.{year}'
        new_entry.append(convert_date)
        bot.send_message(chat_id, text=f'Внесён расход = {new_entry}')
        with open("finances.csv", mode="a", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, lineterminator="\r")
            file_writer.writerow(new_entry)
        new_entry = []
        main_menu()

    global category_message
    if command == "category":
        cat = call.data.split('+')[1]
        if cat == 'Пиво':
            bot.send_message(chat_id, 'А вот это отлично')
        bot.delete_message(chat_id, category_message)
        bot.register_next_step_handler(bot.send_message(chat_id, 'Введите сумму (c для отмены):'), _sum, cat)


def _sum(message, cat):
    if message.text.lower() == 'c' or message.text.lower() == 'с':
        main_menu(message)
    else:
        global new_entry
        new_entry = [cat, message.text]
        bot.register_next_step_handler(bot.send_message(chat_id, 'Введите название (c для отмены):'),
                                       name)


def name(message):
    if message.text.lower() == 'c' or message.text.lower() == 'с':
        main_menu(message)
    else:
        global new_entry
        new_entry.append(message.text)
        show_calendar(message)


def summ_all():
    summ = 0
    with open("finances.csv", mode="r", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, lineterminator="\r")
        for row in file_reader:
            summ += int(row[1])
    bot.send_message(chat_id, text=f'Сумма всех расходов = {summ}')


def last():
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
                last += str(row) + '\n'
    bot.send_message(chat_id, text=f'{last}')


bot.infinity_polling()
