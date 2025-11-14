import aiosqlite
import os

if not os.path.exists("data"):
    os.makedirs("data")

DB_PATH = "data/bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # کاربران
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            balance INTEGER DEFAULT 0,
            total_spent INTEGER DEFAULT 0,
            join_date TEXT,
            level TEXT DEFAULT 'عادی',
            orders_count INTEGER DEFAULT 0
        )''')
        # سرویس‌ها و دسته‌بندی‌ها
        await db.execute('''CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            emoji TEXT
        )''')
        await db.execute('''CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            name TEXT,
            price_usd REAL
        )''')
        # سفارشات
        await db.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            service_name TEXT,
            price_irr INTEGER,
            status TEXT DEFAULT 'در انتظار پرداخت',
            track_code TEXT,
            created_at TEXT
        )''')
        await db.commit()
