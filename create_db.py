"""Создание базы данных и ее поля"""

import sqlite3

conn = sqlite3.connect('hse_food_guide_bot.db')

conn.execute('''CREATE TABLE users
                 (id INTEGER PRIMARY KEY,
                  username TEXT)''')

conn.execute('''CREATE TABLE categories
                 (category TEXT PRIMARY KEY,
                  count INTEGER)''')

conn.execute('''CREATE TABLE reviews
                 (feedback_name TEXT PRIMARY KEY,
                  count INTEGER)''')

# Create promo table
conn.execute('''CREATE TABLE promo
                 (place_name TEXT PRIMARY KEY,
                  count INTEGER)''')


conn.commit()
conn.close()
