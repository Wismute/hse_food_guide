"""Основной файл бота"""

import os
import json
import telebot
from telebot import types
import cherrypy
import sentry_sdk
from dotenv import load_dotenv

import config
import stats
from keyboards import (
    send_categories,
    send_locations,
    send_review_request_and_navigation)

load_dotenv()

TOKEN = os.getenv('TOKEN')
PORT = int(os.getenv('PORT'))
SENTRY_URL = os.getenv('SENTRY_URL')
ADMIN_USERNAMES = os.getenv('ADMIN_USERNAMES').split(',')

LOCATIONS = config.LOCATIONS
SEGMENTS = config.SEGMENTS
CATEGORIES = config.CATEGORIES

sentry_sdk.init(SENTRY_URL, traces_sample_rate=1.0)

bot = telebot.TeleBot(TOKEN)

states = {}


def save_states():
    """Сохранение состояний для перезагрузки"""

    with open('saved_states.txt', 'w', 
              encoding='utf-8') as states_file:
        json.dump(states, states_file)


def load_states():
    """Сохранение состояний для перезагрузки"""
    global states

    with open('saved_states.txt', 'r',
              encoding='utf-8') as states_file:
        states = json.load(states_file)

load_states()


@bot.message_handler(func=lambda message: True, content_types=["text"])
def main(message):
    """Обработчик главной логики"""

    def get_location(user_data):
        """Получение выбранного пользователем корпуса"""

        try:
            return states[user_data]
        except KeyError:
            send_locations(bot, message)
            return None

    username = message.from_user.username
    user_id = message.from_user.id
    user_data = f'{username}/{user_id}'

    if '/start' == message.text:
        stats.register_user(user_id, username)

        bot.send_message(message.chat.id, text=config.HELLO_TEXT)

        send_locations(bot, message)


    # Если была выбрана локация, отправляем категории
    elif message.text in LOCATIONS:
        states.update({user_data: message.text})
        send_categories(bot, message)

    # Если была выбрана категория, устанавливаем ее
    elif message.text in SEGMENTS:
        category = CATEGORIES[message.text.split()[-1]]

    elif '⬅️ Вернуться к категориям' == message.text:
        send_categories(bot, message)

    elif '⬅️ Вернуться к локациям' == message.text:
        send_locations(bot, message)

    # Функции администраторов
    elif username in ADMIN_USERNAMES:

        if 'Статистика' == message.text:
            ans = stats.get_stat()
            bot.send_message(message.chat.id, text=ans,
                             parse_mode='Markdown')

        if 'save' == message.text.lower():
            save_states()


    # Если была выбрана категория,
    # создаем клавиатуру из заведений
    # для выбранного корпуса и самой категории
    elif message.text in SEGMENTS:

        # Подтверждаем выбранную категорию
        bot.send_message(message.chat.id, message.text)

        # Засчитываем выбранную категорию в статистику
        stats.category_tap(category)

        # Получаем выбранный корпус
        location = get_location(user_data)

        # Создаем и отправляем клавиатуру с заведениями
        if location:
            with open(f"{location}/{category}/index.txt",
                      "r", encoding="utf-8") as f:
                places_names = f.read().split('\n')

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            # Индексы первого и второго заведения в линии клавиатуры
            x = 0
            y = 1

            # Граничный случай для единственного заведения в категории
            if round(len(places_names)/2) == 0:
                markup.row(places_names[x])

            # Для всех остальных формируем клавиатуру
            # В каждой линии два заведения
            #
            # Если количество заведений нечетное,
            # то последнее заведение остается на всю ширину клавиатуры
            else:

                for i in range(round(len(places_names)/2)):
                    try:
                        markup.row(places_names[x], places_names[y])
                        x += 2
                        y += 2
                    except IndexError:
                        markup.row(places_names[x])

            markup.row('⬅️ Вернуться к категориям')
            markup.row('⬅️ Вернуться к локациям')

            ans = '*Выберите конкретное заведение*\nдля получения подробной информации'
            bot.send_message(message.chat.id, text=ans,
                             reply_markup=markup, parse_mode='Markdown')

        # Или даем его выбрать
        else:
            send_locations(bot, message)

    # Все остальные сообщения считаем названием выбранного заведения
    # Находим нужное заведение и отправляем всю информацию о нем
    else:

        location = get_location(user_data)

        if location:

            # Учет количества нажатий на выделенные огнем заведения
            if message.text.startswith('🔥 '):
                stats.promo_count(message.text[1::])

            with open(f'{location}/{category}/list.txt', 'r', encoding="utf-8") as f:
                places = f.read().split('<br>\n')

            for place in places:

                if message.text.startswith(place):

                    bot.send_message(message.chat.id, text=i,
                                     parse_mode='Markdown')
                    send_review_request_and_navigation(bot, message)
                    break


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """Обработчик кнопок inline-клавиатур"""

    if call.message:

        if 'useful' == call.data:
            stats.useful()
            bot.send_message(call.message.chat.id,
                             text='Спасибо за отзыв! (+)')

        elif 'not_useful' == call.data:
            stats.not_useful()
            bot.send_message(call.message.chat.id,
                             text='Спасибо за отзыв! (-)')

        elif 'back_to_categories' == call.data:
            send_categories(bot, call.message)

        elif 'back_to_locations' == call.data:
            send_locations(bot, call.message)


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        """Создаем эндпоинт для вебхука"""

        length = int(cherrypy.request.headers['content-length'])
        json_string = cherrypy.request.body.read(length).decode("utf-8")
        update = telebot.types.Update.de_json(json_string)

        bot.process_new_updates([update])
        return ''


if __name__ == '__main__':

    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': PORT
    })

    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
