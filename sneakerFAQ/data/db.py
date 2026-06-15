import sqlite3
from app.cfg import DB_PATH
from app.log import print_log

def init_data_base():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sneakers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL
                )
            """)
        
        conn.commit()
    print_log(level_log='info', text='База данных успешна создана')

def insert_obj(table: str, data: dict):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)

        conn.commit()
    print_log(level_log='info', text='Данные успешно добавлены')


def get_all_sneakers():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, price FROM sneakers")
        items = cursor.fetchall()  
    return items