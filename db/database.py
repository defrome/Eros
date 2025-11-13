import sqlite3

from config import DB_URL

async def db_func():
    try:
        with sqlite3.connect(f"{DB_URL}") as conn:
            cursor = conn.cursor()

            cursor.execute("""CREATE TABLE user_info
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                            value INTEGER, 
                            status BOOL)
                        """)

            user_data = (0, True)
            cursor.execute(
                "INSERT INTO user_info (value, status) VALUES (?, ?)",
                user_data
            )

    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")