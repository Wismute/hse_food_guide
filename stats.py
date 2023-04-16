"""Ведение статистики и работа с базой данных"""

import sqlite3

DB_FILENAME = 'hse_food_guide_bot.db'

def register_user(user_id, username):
    """Добавляем нового пользователя в базу данных"""

    with sqlite3.connect(DB_FILENAME) as conn:

        conn.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)",
                     (user_id, username))
        conn.commit()


def get_stat():
    """Получение текста статистики для отправки"""

    with sqlite3.connect(DB_FILENAME) as conn:

        ans = ''

        # Получаем количество уникальных пользователей
        cursor = conn.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]

        ans += f'Уникальных пользователей: {user_count}\n\n'

        # Получаем количество отзывов
        cursor = conn.execute('SELECT * FROM reviews')
        rows = cursor.fetchall()

        ans += f'Полезно: {rows[0][1]}\nБесполезно: {rows[1][1]}'

    return ans


def category_tap(category):
    """Учитываем нажатие на категорию"""

    with sqlite3.connect(DB_FILENAME) as conn:

        conn.execute("INSERT OR IGNORE INTO categories (category, count) VALUES (?, ?)",
                     (category, 1))
        conn.execute("UPDATE categories SET count = count + 1 WHERE category = ?",
                     (category,))
        conn.commit()


def useful():
    """Учитываем нажатие на Полезно"""

    with sqlite3.connect(DB_FILENAME) as conn:

        conn.execute("UPDATE reviews SET count = count + 1 WHERE feedback_name = 'useful'")
        conn.commit()


def not_useful():
    """Учитываем нажатие на Бесполезно"""

    with sqlite3.connect(DB_FILENAME) as conn:

        conn.execute("UPDATE reviews SET count = count + 1 WHERE feedback_name = 'not_useful'")
        conn.commit()

def promo_count(placename):
    """Учитываем нажатие на категорию"""

    with sqlite3.connect(DB_FILENAME) as conn:

        conn.execute("INSERT OR IGNORE INTO promo (place_name, count) VALUES (?, ?)",
                     (placename, 1))
        conn.execute("UPDATE promo SET count = count + 1 WHERE place_name = (?)", (placename,))
        conn.commit()
