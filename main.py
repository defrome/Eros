import asyncio

from db.database import create_database

asyncio.run(create_database())