"""Основные тексты и параметры бота"""


LOCATIONS = [
    'Мясницкая', 'Шаболовская', 'Ордынка', 'Басманная',
    'Покровка', 'Харитоновский', 'Б. Трехсвятительский',
    'Хитровский', 'Вавилова', 'Таллинская', 'Гнездниковский пер',
    'Пионерская', 'Трифоновская', 'Усачева', 'Лялин пер', 'Колобовский пер'
]

SEGMENTS = [
    'Бары 🍹', 'Шаурма 🌯',
    'Магазины с готовой едой 🍲',
    'Кофейни ☕', 'Фастфуд 🍔',
    'Кафе и рестораны 🍴'
]

CATEGORIES = {
    '🍹': 'Бары',
    '🌯': 'Шаурма',
    '☕': 'Кофейни',
    '🍔': 'Фастфуд',
    '🍴': 'Кафе и рестораны',
    '🍲': 'Магазины с готовой едой'
}

HELLO_TEXT = '''
Привет!

Давай найдем куда сходить сегодня.

Подсказать нам, где мы ошиблись или что-то упустили можно в нашем боте поддержки @HFBSBOT или написав сюда *Помощь* или *Саппорт* 😊
'''