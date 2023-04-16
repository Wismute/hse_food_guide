"""Клавиатуры выбора"""

from telebot import types

def send_categories(bot, message):
    """Отправка клавиатуры с категориями заведений"""

    ans = '*Выбери категорию еды:*'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row('Бары 🍹', 'Шаурма 🌯')
    markup.row('Кофейни ☕', 'Фастфуд 🍔')
    markup.row('Кафе и рестораны 🍴')
    markup.row('Магазины с готовой едой 🍲')
    markup.row('⬅️ Вернуться к локациям')

    bot.send_message(message.chat.id, text=ans,
                    reply_markup=markup, parse_mode='Markdown')

def send_locations(bot, message):
    """Отправка клавиатуры с выбором корпуса """

    ans = '*Выбери локацию:*'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row('Мясницкая', 'Шаболовская')
    markup.row('Ордынка', 'Басманная')
    markup.row('Покровка', 'Харитоновский')
    markup.row('Хитровский', 'Вавилова')
    markup.row('Колобовский пер', 'Лялин пер')
    markup.row('Б. Трехсвятительский', 'Гнездниковский пер')
    markup.row('Пионерская', 'Трифоновская')
    markup.row('Усачева', 'Таллинская')

    bot.send_message(message.chat.id, text=ans,
                    reply_markup=markup, parse_mode='Markdown')

def send_review_request_and_navigation(bot, message):
    """Отправка запроса оценки и
    дополнительных элементов навигации

    """

    keyboard = types.InlineKeyboardMarkup()

    callback_button_1 = types.InlineKeyboardButton(
        text="Полезно",
        callback_data="useful")

    callback_button_2 = types.InlineKeyboardButton(
        text="Бесполезно",
        callback_data="not_useful")

    callback_button_3 = types.InlineKeyboardButton(
        text="⬅️ Вернуться к категориям",
        callback_data="back_to_categories")

    callback_button_4 = types.InlineKeyboardButton(
        text="⬅️ Вернуться к локациям",
        callback_data="back_to_locations")

    keyboard.add(callback_button_1)
    keyboard.add(callback_button_2)
    keyboard.add(callback_button_3)
    keyboard.add(callback_button_4)

    ans = 'Была ли эта информация полезной?'
    bot.send_message(chat_id=message.chat.id, text=ans,
                    reply_markup=keyboard)
