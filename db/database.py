import sqlite3

from config import DB_URL

con = sqlite3.connect(f"{DB_URL}")
cursor = con.cursor()

cursor.execute("""CREATE TABLE user_info
                (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                value INTEGER, 
                status BOOL)
            """)
print("Таблицы созданы.")