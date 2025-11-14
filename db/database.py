import sqlite3

from config import DB_URL

def db_func():
    try:
        with sqlite3.connect(f"{DB_URL}") as conn:
            cursor = conn.cursor()

            cursor.execute("""CREATE TABLE user_info
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                            value INTEGER, 
                            status BOOL,
                            last_gift TEXT)
                        """)

            user_data = (0, True, "zero")
            cursor.execute(
                "INSERT INTO user_info (value, status, last_gift) VALUES (?, ?, ?)",
                user_data
            )

    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")