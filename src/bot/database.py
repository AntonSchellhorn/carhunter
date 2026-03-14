import aiosqlite

DB_PATH = "carhunter.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS searches (
                user_id     INTEGER PRIMARY KEY,
                make        TEXT,
                model       TEXT,
                year_from   INTEGER,
                year_to     INTEGER,
                price_max   INTEGER,
                mileage_max INTEGER,
                is_active   INTEGER DEFAULT 0
            )
        """)
        await db.commit()


async def save_search(user_id, make, model, year_from, year_to, price_max, mileage_max):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO searches
                (user_id, make, model, year_from, year_to, price_max, mileage_max, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            ON CONFLICT(user_id) DO UPDATE SET
                make        = excluded.make,
                model       = excluded.model,
                year_from   = excluded.year_from,
                year_to     = excluded.year_to,
                price_max   = excluded.price_max,
                mileage_max = excluded.mileage_max,
                is_active   = 1
        """, (user_id, make, model, year_from, year_to, price_max, mileage_max))
        await db.commit()


async def get_search(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM searches WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def set_active(user_id, active):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE searches SET is_active = ? WHERE user_id = ?",
            (1 if active else 0, user_id)
        )
        await db.commit()