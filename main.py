#!/usr/bin/python
# -*- coding: utf-8 -*-

import telegram
import requests
import json
import pytz
import datetime as dt
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, BaseFilter
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
import wr
import logging
import time
import totable
import random
import datetime
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '707090914:AAFOupGmBjkNIkaZp81IEflkHuDiZgbqOWk'
REQUEST_KWARGS={
    'proxy_url': 'socks5://exp1.s5overss.mtpro.xyz:39610',
    'urllib3_proxy_kwargs': {
        'username': 'mtpro_xyz',
        'password': 'mtpro_xyz_bot',
    }
}
updater = Updater(token=TOKEN, request_kwargs=REQUEST_KWARGS)
updates = updater
dispatcher = updater.dispatcher
FR = telegram.ForceReply()


@run_async
def confirmation(bot, updater):
    time.sleep(random.uniform(0, 0.7))
    players = wr.read_results()
    if str(updater.message.chat.id) in players:
        bot.send_message(chat_id=updater.message.chat.id,
                         text='Йо, ты уже в системе. Просто используй команды.')
    else:
        btnlist = [
            telegram.InlineKeyboardButton('Согласен.', callback_data='agree')
        ]
        markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=1))
        bot.send_message(chat_id=updater.message.chat.id,
                         text='Для начала необходимо согласиться с Согласием на обработку персональный данных.')
        bot.send_message(chat_id=updater.message.chat.id,
                         text='Я даю своё согласие на обработку и публикацию моих персональных данных, таких как: результат участия в Экономической Карусели, никнейм Экономической Карусели, никнейм в Телеграме.',
                         reply_markup=markup)


@run_async
def get_nick(bot, updater):
    time.sleep(random.uniform(0, 0.7))
    players = wr.read_results()
    id = updater.message.chat.id
    name = updater.message.text
    players[str(id)] = players[str(id)]+[name, {}, []]
    wr.write_results(players)
    btnlist = [
        telegram.InlineKeyboardButton('Меню.', callback_data='menu')
    ]
    markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=1))
    bot.send_message(chat_id=updater.message.chat.id, text='Привет, {}!'.format(name), reply_markup=markup)


@run_async
def query_h(bot, updater,):
    call = updater.callback_query
    if call.message:
        if call.data == 'agree':
            time.sleep(random.uniform(0, 0.7))
            players = wr.read_results()
            id = call.message.chat.id
            message_id = call.message.message_id
            bot.edit_message_text(chat_id=id, message_id=message_id,
                                  text=call.message.text)
            if str(id) not in players:
                players[str(id)] = [id, '@' + str(call.message.chat.username)]
                bot.send_message(chat_id=id,
                                 text='А теперь давайте познакомимся. Под каким никнеймом отображать вас в таблице результатов?',
                                 reply_markup=FR)
            else:
                bot.send_message(chat_id=id, text='Ты уже в системе, вот меню!')
                show_menu(bot, updater)
            wr.write_results(players)
        if call.data =='contest':
            print_list(bot,updater)
        if call.data == 'past':
            bot.send_document(chat_id=call.message.chat.id, document=open('pdf.pdf', 'rb'))
            pass
        if call.data == 'other':
            feedback(bot, updater)
        if call.data == 'rules':
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            btnlist = [
                telegram.InlineKeyboardButton('Общие Правила.', callback_data='general'),
                telegram.InlineKeyboardButton('Карусель ЛЭШ.', callback_data='school'),
                telegram.InlineKeyboardButton('Назад.', callback_data='menu')
            ]
            markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=1))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                             text='Правила:', reply_markup=markup)
        if call.data == 'general':
            print_rules(bot, updater, 0)
        if call.data == 'school':
            print_rules(bot, updater, 1)
        if call.data == 'menu':
            show_menu(bot, updater)
        if call.data == 'fb':
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=call.message.text)
            bot.send_message(chat_id=call.message.chat.id, text='Оставьте свой отзыв ответом на это сообщение.', reply_markup=FR)
        if call.data == 'donate':
            donate(bot, updater)
        if call.data == 'probs':
            problems_list(bot, updater)
        if call.data == 'admin':
            admin(bot, updater)
        if call.data == 'addadmin':
            id = call.message.chat.id
            message_id = call.message.message_id
            bot.edit_message_text(chat_id=id, message_id=message_id, text=call.message.text)
            bot.send_message(chat_id=id, text='Напишите ник нового админа ответом на это сообщение.', reply_markup=FR)
        if call.data[:3] == 'pr_':
            problems = wr.read_problems()
            id = call.message.chat.id
            message_id = call.message.message_id
            grouped = []
            dates = []
            if problems[call.data[3:]][2] == []:
                dates = list(range(10, 28))
            else:
                dates = problems[call.data[3:]][2]
            for d in wr.group_consecutives(dates):
                if type(d) == list:
                    grouped.append('с {} по {}'.format(d[0], d[-1]))
                else:
                    grouped.append(str(d))
            dates = ', '.join(grouped)
            btnlist = [
                telegram.InlineKeyboardButton('Удалить.', callback_data='del_{}'.format(call.data[3:])),
                telegram.InlineKeyboardButton('Назад.', callback_data='probs')
            ]
            markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=1))
            bot.edit_message_text(chat_id=id, message_id=message_id,
                                  text='Задача {}\n'.format(call.data[3:])+problems[call.data[3:]][0]+'\nОтвет: '+problems[call.data[3:]][1]+'\nДаты: '+dates, reply_markup=markup)
        # if call.data[:5] == 'hide_':
        #     id = call.message.chat.id
        #     message_id = call.message.message_id
        #     btnlist = [
        #         telegram.InlineKeyboardButton('Показать текст задачи.', callback_data='pr_{}'.format(call.data[5:]))
        #     ]
        #     markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=1))
        #     bot.edit_message_text(chat_id=id, message_id=message_id, text=call.data[5:], reply_markup=markup)

        if call.data == 'list':
            part_list(bot, updater)
        if call.data[:4] == 'add_':
            problems = wr.read_problems()
            btnlist = []
            for problem in problems:
                btnlist.append(telegram.InlineKeyboardButton(problem, callback_data='ch_pr_{}'.format(problem)))
            footer = telegram.InlineKeyboardButton('Назад.', callback_data='list')
            markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=4, footer_buttons=[footer]))
            id = call.message.chat.id
            message_id = call.message.message_id
            players = wr.read_results()
            bot.edit_message_text(chat_id=id, message_id=message_id, text='Участник {}'.format(players[str(id)][2]), reply_markup=markup)
        if call.data[:6] == 'ch_pr_':
            id = call.message.chat.id
            message_id = call.message.message_id
            players = wr.read_results()
            btnlist = []
            for date in range(5, 32):
                if date not in range(10,28):
                    date = '-{}-'.format(date)
                if call.data[6:] in players[str(id)][3]:
                    if date in players[str(id)][3][call.data[6:]]:
                        date = '+{}+'.format(date)
                btnlist.append(telegram.InlineKeyboardButton(date, callback_data='date_{}'.format(date)))
            btnlist.append(telegram.InlineKeyboardButton('-1-', callback_data='aaaaa'))
            btnlist.append(telegram.InlineKeyboardButton('Назад', callback_data='add_{}'.format(call.data[6:])))
            btnlist.append(telegram.InlineKeyboardButton('Обновить', callback_data='ch_pr_{}'.format(call.data[6:])))
            markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=7))
            bot.edit_message_text(chat_id=id, message_id=message_id,
                                  text='Участник {}'.format(players[str(id)][2])+'\nЗадача {}'.format(call.data[6:]), reply_markup=markup)
        if call.data[:5] == 'date_':
            id = call.message.chat.id
            message_id = call.message.message_id
            players = wr.read_results()
            text = call.message.text
            problem = text[text.find('Задача')+7:]
            date = call.data[5:]
            if date[0] == '-':
                bot.send_message(chat_id=id, text='Неправильная дата')
            else:
                if date[0] == '+':
                    players[str(id)][3][problem].pop(players[str(id)][3][problem].index(int(date[1:-1])))

                else:
                    try:
                        players[str(id)][3][problem].append(int(date))
                    except KeyError:
                        players[str(id)][3][problem] = [int(date)]
                wr.write_results(players)
#                bot.send_message(chat_id=id, text='Для обновления данных нажмите кнопку \"Обновить.\"')
        if call.data[:3] == 'sh_':
            num = call.data[3:]
            print_problem(bot, updater, num)
        if call.data == 'again':
            problems = wr.read_problems()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=problems[call.message.text[25:-2]][0])
            bot.send_message(chat_id=call.message.chat.id, text='Ваш ответ к задаче {} :'.format(call.message.text[25:-2]), reply_markup=FR)
        if call.data == 'solved':
            players = wr.read_results()
            btnlist = []
            for pr in players[str(call.message.chat.id)][4]:
                btnlist.append(telegram.InlineKeyboardButton(pr, callback_data='s_{}'.format(pr)))
            footer = telegram.InlineKeyboardButton('Назад.', callback_data='contest')
            markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=2, footer_buttons=[footer]))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Ваши решенные задачи!', reply_markup=markup)
        if call.data[:2] == 's_':
            problems = wr.read_problems()
            num = call.data[2:]
            markup = telegram.InlineKeyboardMarkup(wr.build_menu([telegram.InlineKeyboardButton('Назад.', callback_data='solved')], n_cols=1))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Задача {}\n'.format(num)+str(problems[num][0])+'\n'+'Ответ: {}'.format(problems[num][1]),
                                  reply_markup=markup)
        if call.data == 'error':
            markup = telegram.InlineKeyboardMarkup(wr.build_menu([telegram.InlineKeyboardButton('Назад.', callback_data='contest')], n_cols=1))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Вы пока не можете решать эту задачу.',
                                  reply_markup=markup)
        if call.data == 'addtask':
            markup = telegram.InlineKeyboardMarkup(wr.build_menu([telegram.InlineKeyboardButton('probs.', callback_data='solved')], n_cols=1))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Читай ниже.')
            bot.send_message(chat_id=call.message.chat.id, text='Отправьте текст задачи и ответ ответом на это сообщение.', reply_markup=FR)
        if call.data[:4] == 'del_':
            problems = wr.read_problems()
            problem = call.data[4:]
            del(problems[problem])
            wr.write_problems(problems)
            markup = telegram.InlineKeyboardMarkup(
                wr.build_menu([telegram.InlineKeyboardButton('Назад.', callback_data='probs')], n_cols=1))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Задача успешно удалена.',
                                  reply_markup=markup)
        if call.data == 'send_res':
            send_res(bot, updater)
        if call.data == 'send_fb':
            send_fb(bot, updater)
        if call.data == 'repost':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Смотрите ниже.')
            bot.send_message(chat_id=call.message.chat.id, text='Ответьте на это сообщение тем, что хотите всем разослать.', reply_markup=FR)


@run_async
def print_rules(bot, updater, *version):
    chat_id = updater.callback_query.message.chat.id
    message_id = updater.callback_query.message.message_id
    btnlist = [
        telegram.InlineKeyboardButton('Общие Правила.', callback_data='general'),
        telegram.InlineKeyboardButton('Карусель ЛЭШ.', callback_data='school'),
        telegram.InlineKeyboardButton('Назад.', callback_data='menu')
    ]
    markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=1))
    if version[0] == 0:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='''*Как сдавать ответ:*

Во время тура необходимо ответить боту на сообщение вида:\n\"Ваш ответ к задаче # :\"\n*сообщинем с только ответом на задачу*, которым будет являться десятичное число. *Числа записываются в виде десятичной дроби с математическим округлением до двух знаков после запятой, через точку*.

*Ход тура и подведение его итогов:*

Время, которое даётся на решение задач, ограничено временем проведения тура.

Вопросы по условию можно задавать на протяжении всего тура в вк:
Александр - vk.com/sashashivarov

Во время тура Вы получаете задание, решаете его и даете только ответ. Независимо от результата (верный ответ или нет), Вы получаете следующее задание. 

Время на решение каждого задания не ограничено, определено только общее время проведения тура.

Процесс решения заканчивается, если Вы прошли все задачи или если закончилось время на решение.

Места распределяются согласно количеству набранных баллов. Если кто-то набирает равное количество баллов, то выше ставится тот, у которого больше верных ответов.

*Начисление баллов:*

Первая задача стоит 3 балла.

Если к задаче дан верный ответ, то Вы получает её полную стоимость, а следующая задача будет стоить на 1 балл больше. 

Если на задачу дан неверный ответ, то команда получает за решение 0 баллов, а следующая задача будет стоить на 3 балла меньше (но не менее 3 баллов она стоить не может).

По всем техническим вопросам - vk.com/coolkaos, @CoolkaOS'''
'', parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=markup)
    else:

        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='''ПОЗЖЕ''', reply_markup=markup)


@run_async
def show_menu(bot, updater):
    time.sleep(random.uniform(0, 0.7))
    btnlist = [
        telegram.InlineKeyboardButton('Начать Контест!', callback_data='contest'),
        telegram.InlineKeyboardButton('Задания прошлых Каруселей', callback_data='past'),
        telegram.InlineKeyboardButton('Правила.', callback_data='rules'),
        telegram.InlineKeyboardButton('Поддержать проект/Оставить отзыв.', callback_data='other')
    ]
    markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=1))
    if 'callback_query' in str(updater):
        chat_id = updater.callback_query.message.chat.id
        message_id = updater.callback_query.message.message_id
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Меню:', reply_markup=markup)
    else:
        chat_id = updater.message.chat.id
        bot.send_message(chat_id=chat_id, text='Меню.', reply_markup=markup)


@run_async
def print_problem(bot, updater, num):
    problems = wr.read_problems()
    id = updater.callback_query.message.chat.id
    message_id = updater.callback_query.message.message_id
    if num == 'end':
        #results
        pass
    else:
        bot.edit_message_text(chat_id=id, message_id=message_id, text='Задача {}\n'.format(num)+str(problems[num][0]))
        bot.send_message(chat_id=id, text='Ваш ответ к задаче {} :'.format(num), reply_markup=FR)


class FilterNick(BaseFilter):
    def filter(self, message):
        try:
            return 'А теперь давайте познакомимся. Под каким никнеймом отображать вас в таблице результатов?' == message.reply_to_message.text
        except AttributeError:
            return False
filter_nick = FilterNick()


class FilterFB(BaseFilter):
    def filter(self, message):
        try:
            return 'Оставьте свой отзыв ответом на это сообщение.' == message.reply_to_message.text
        except AttributeError:
            return False

filter_fb = FilterFB()


class FilterAns(BaseFilter):
    def filter(self, message):
        try:
            return 'Ваш ответ к задаче' == message.reply_to_message.text[:18]
        except AttributeError:
            return False

filter_ans = FilterAns()

class FilterAA(BaseFilter):
    def filter(self, message):
        try:
            return 'Напишите ник нового админа ответом на это сообщение.' == message.reply_to_message.text
        except AttributeError:
            return False

filter_aa = FilterAA()


class FilterAT(BaseFilter):
    def filter(self, message):
        try:
            return 'Отправьте текст задачи и ответ ответом на это сообщение.' == message.reply_to_message.text
        except AttributeError:
            return False

filter_at = FilterAT()


class FilterRep(BaseFilter):
    def filter(self, message):
        try:
            return 'Ответьте на это сообщение тем, что хотите всем разослать.' == message.reply_to_message.text
        except AttributeError:
            return False

filter_rep = FilterRep()

@run_async
def feedback(bot, updater):
    time.sleep(random.uniform(0, 0.7))
    id = updater.callback_query.message.chat.id
    message_id = updater.callback_query.message.message_id
    btnlist = [
        telegram.InlineKeyboardButton('Поддержать проект.', callback_data='donate'),
        telegram.InlineKeyboardButton('Через Бота.', callback_data='fb'),
        telegram.InlineKeyboardButton('Через Google Forms.', url='google.com')
    ]
    footer = telegram.InlineKeyboardButton('Назад.', callback_data='menu')
    markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=3, footer_buttons=[footer]))
    bot.edit_message_text(
        chat_id=id, message_id= message_id,
        text='Выберите, как вы хотите оставить отзыв, или хотите поддержать проект?',
        reply_markup=markup)


@run_async
def thx_fb(bot, updater):
    time.sleep(random.uniform(0, 0.7))
    fb = wr.read_feedback()
    if str(updater.message.from_user.id) in fb:
        fb[str(updater.message.from_user.id)].append(updater.message.text)
    else:
        fb[str(updater.message.from_user.id)] = [updater.message.text]
    bot.send_message(chat_id=updater.message.chat.id, text='Спасибо за отзыв! ')
    wr.write_feedback(fb)
    show_menu(bot, updater)


@run_async
def donate(bot, updater):
    time.sleep(random.uniform(0, 0.7))
    id = updater.callback_query.message.chat.id
    message_id = updater.callback_query.message.message_id
    btnlist = [
        telegram.InlineKeyboardButton('Назад.', callback_data='other')
    ]
    markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=1))
    bot.edit_message_text(chat_id=id,
                          message_id=message_id,
                          text='Поддержать проект можно через нашу страничку ВК \n(https://vk.com/economic_carousel) или переводом в Сбребанк Онлайн.', reply_markup=markup)
    bot.send_message(chat_id=id, text='2202 2011 4263 4639')

@run_async
def rest(bot, updater):
    bot.send_message(chat_id=updater.message.chat.id, text='Ауч!')


@run_async
def clear(bot, updater):
    try:
        wr.clear(str(updater.message.chat.id))
    except KeyError:
        pass
    bot.send_message(chat_id=updater.message.chat.id, text='Чисто.')


@run_async
def admin(bot, updater):
    players = wr.read_results()
    btnlist = [
        telegram.InlineKeyboardButton('Показать список участников.', callback_data='list'),
        telegram.InlineKeyboardButton('Показать задачи.', callback_data='probs'),
        telegram.InlineKeyboardButton('Добавить админа.', callback_data='addadmin'),
        telegram.InlineKeyboardButton('Отправить результаты.', callback_data='send_res'),
        telegram.InlineKeyboardButton('Отправить отзывы.', callback_data='send_fb'),
        telegram.InlineKeyboardButton('Отправить всем сообщение через бота.', callback_data='repost')
    ]
    markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=1))
    if 'callback_query' in str(updater):
        id = updater.callback_query.message.chat.id
        message_id = updater.callback_query.message.message_id
        bot.edit_message_text(chat_id=id, message_id=message_id,
                         text='Мeню Админа.',
                         reply_markup=markup)
    elif players[str(updater.message.chat.id)][1] not in wr.read_admins():
        id = updater.message.chat.id
        bot.send_message(chat_id=id, text='У вас нет доступа к данным функциям!')
    else:
        id = updater.message.chat.id
        bot.send_message(chat_id=id,
                         text='Мeню Админа.',
                         reply_markup=markup)


@run_async
def problems_list(bot, updater):
    problems = wr.read_problems()
    btnlist = []
    for problem in problems:
        btnlist.append(telegram.InlineKeyboardButton(problem, callback_data='pr_{}'.format(problem)))
    footer = [telegram.InlineKeyboardButton('Добавить задачу.', callback_data='addtask'),
              telegram.InlineKeyboardButton('Назад.', callback_data='admin')]
    markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=4, footer_buttons=footer))
    bot.edit_message_text(chat_id=updater.callback_query.message.chat.id,
                          message_id=updater.callback_query.message.message_id,
                          text='Задачи:', reply_markup=markup)



@run_async
def part_list(bot, updater):
    players = wr.read_results()
    btnlist = []
    for id in players:
        btnlist.append(telegram.InlineKeyboardButton(players[id][2], callback_data='add_{}'.format(updater.callback_query.message.chat.id)))
    footer = telegram.InlineKeyboardButton('Назад.', callback_data='admin')
    markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=2, footer_buttons=[footer]))
    bot.edit_message_text(chat_id=updater.callback_query.message.chat.id, message_id=updater.callback_query.message.message_id, text='Список участников.', reply_markup=markup)


@run_async
def add_admin(bot, updater):
    admins = wr.read_admins()
    admins.append(updater.message.text)
    wr.write_admins(admins)
    bot.send_message(chat_id=updater.message.chat.id, text='Админ {} добавлен!'.format(updater.message.text))


@run_async
def print_list(bot, updater):
    problems = wr.read_problems()
    id = updater.callback_query.message.chat.id
    message_id = updater.callback_query.message.message_id
    players = wr.read_results()
    for i in range(1, 10):
        if i in list(int(pr[:1]) for pr in problems.keys()):
            ran = problems["{}.1".format(i)][2]
            if ran == []:
                ran = list(range(10, 28))
            if "{}.1".format(i) not in players[str(id)][4]:
                players[str(id)][3]["{}.1".format(i)] = ran
    btnlist = []
    for pr in problems:
        if pr in players[str(id)][3]:
            grouped = []
            for d in wr.group_consecutives(players[str(id)][3][pr]):
                if type(d) == list:
                    grouped.append('с {} по {}'.format(d[0], d[-1]))
                else:
                    grouped.append(str(d))
            dates = ', '.join(grouped)
            if datetime.datetime.today().day in players[str(id)][3][pr]:
#            if 10 in players[str(id)][3][pr]:
                btnlist.append(telegram.InlineKeyboardButton('*{}* на даты {}'.format(pr, dates),
                                                             callback_data='sh_{}'.format(pr)))
            else:
                btnlist.append(telegram.InlineKeyboardButton('-{}- на даты {}'.format(pr, dates),
                                                             callback_data='error'))
    footer = [telegram.InlineKeyboardButton('Показать решённые задачи.', callback_data='solved'), telegram.InlineKeyboardButton('Назад.', callback_data='menu')]
    markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=1, footer_buttons=footer))
    bot.edit_message_text(chat_id=id, message_id=message_id, text='Выберете задачу:\n-__- значит, что пока задача не доступна для решения.\n*__* значит, что задача доступна.', reply_markup=markup)
    wr.write_results(players)


@run_async
def answer_problem(bot, updater):
    problems = wr.read_problems()
    answer = updater.message.text
    problem = updater.message.reply_to_message.text[19:-2]
    pr_1 = problem[:2]
    pr_2 = problem[2:]
    try:
        float(answer)
        players = wr.read_results()
        if answer == problems[problem][1]:
            rep = 'Ответ верный!'
            btnlist = [
                telegram.InlineKeyboardButton('Назад', callback_data='contest')
            ]
            del(players[str(updater.message.chat.id)][3][problem])
            players[str(updater.message.chat.id)][4].append(problem)
            if int(pr_2) < len(list(key for key in problems if key[:1] == pr_1)):
                players[str(updater.message.chat.id)][3][pr_1+str(int(pr_2)+1)] = problems[pr_1+str(int(pr_2)+1)][2]
            wr.write_results(players)
        else:
            rep = 'Ответ неверный на задачу {} !'.format(problem)
            btnlist =[
                telegram.InlineKeyboardButton('Ещё раз.', callback_data='again'),
                telegram.InlineKeyboardButton('Назад', callback_data='contest')
            ]
        markup = telegram.InlineKeyboardMarkup(wr.build_menu(btnlist, n_cols=1))
        bot.send_message(chat_id=updater.message.chat.id, text=rep, reply_markup=markup)
    except ValueError:
        bot.send_message(chat_id=updater.message.chat.id, text='Неправильный формат ответа!')
        bot.send_message(chat_id=updater.message.chat.id, text=updater.message.reply_to_message.text)


@run_async
def add_task(bot, updater):
    problems = wr.read_problems()
    problem = updater.message.text
    answer_ind = problem.find('Ответ: ')
    dates_ind = problem.find('Даты:')
    num_ind = problem.find('\n')
    num = problem[7:num_ind]
    if dates_ind != -1:
        answer = problem[answer_ind + 7:dates_ind - 1]
        pre_dat = ''.join(problem[dates_ind+5:].split())
        dates = pre_dat.split(',')
        if dates == ['']:
            fin_dates = []
        else:
            fin_dates = list(int(d) for d in dates)
    else:
        fin_dates = []
        answer = problem[answer_ind + 7:]
    problem = problem[num_ind+1:answer_ind-1]
    problems[num] = [problem, answer, fin_dates]
    wr.write_problems(problems)
    markup = telegram.InlineKeyboardMarkup(
    wr.build_menu([telegram.InlineKeyboardButton('Назад.', callback_data='probs')], n_cols=1))
    bot.send_message(chat_id=updater.message.chat.id, text='Задача успешно добавлена.', reply_markup=markup)


def send_res(bot, updater):
    doc = open('results.json', 'rb')
    bot.send_document(chat_id=updater.callback_query.message.chat.id, document=doc)


def send_fb(bot, updater):
    doc = open('feedback.json', 'rb')
    bot.send_document(chat_id=updater.callback_query.message.chat.id, document=doc)


def repost(bot, updater):
    mess = updater.message.text
    for id in wr.read_results():
        try:
            bot.send_message(chat_id=id, text=mess)
        except telegram.error.Unauthorized:
            pass
    markup = telegram.InlineKeyboardMarkup(
        wr.build_menu([telegram.InlineKeyboardButton('Назад.', callback_data='admin')], n_cols=1))
    bot.send_message(chat_id=updater.message.chat.id, text='Успешно!', reply_markup=markup)


dispatcher.add_handler(CallbackQueryHandler(query_h))
dispatcher.add_handler(CommandHandler('start', confirmation))
dispatcher.add_handler(CommandHandler('admin', admin))
dispatcher.add_handler(CommandHandler('menu', show_menu))
dispatcher.add_handler(CommandHandler('predict', clear))
dispatcher.add_handler(MessageHandler(filter_nick, get_nick))
dispatcher.add_handler(MessageHandler(filter_fb, thx_fb))
dispatcher.add_handler(MessageHandler(filter_aa, add_admin))
dispatcher.add_handler(MessageHandler(filter_at, add_task))
dispatcher.add_handler(MessageHandler(filter_ans, answer_problem))
dispatcher.add_handler(MessageHandler(filter_rep, repost))
dispatcher.add_handler(MessageHandler(Filters.chat, rest))
updater.start_polling()
