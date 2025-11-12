import aiosqlite

async def create_database():
    async with aiosqlite.connect("osnova.db") as con:
        async with con.cursor() as cursor:

            await cursor.execute("""CREATE TABLE IF NOT EXISTS user_info
                                  (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                                  nickname TEXT, 
                                  status BOOLEAN)
                                  """)

            await cursor.execute("""CREATE TABLE IF NOT EXISTS gift_info
                                              (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                                              name TEXT, 
                                              status BOOLEAN)
                                              """)

            await con.commit()
        print("Таблица создана успешно!")