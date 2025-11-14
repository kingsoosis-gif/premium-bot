import aiosqlite
import os

if not os.path.exists("data"):
    os.makedirs("data")

DB_PATH = "data/bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            balance INTEGER DEFAULT 0,
            total_spent INTEGER DEFAULT 0,
            join_date TEXT,
            level TEXT DEFAULT 'عادی'
        )""")
        await db.execute("""CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )""")
        await db.commit()
