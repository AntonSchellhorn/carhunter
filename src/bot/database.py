import aiosqlite

DB_PATH = "carhunter.db"


async def init_db():
    """Создаёт таблицы при первом запуске."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Таблица настроек поиска пользователей
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
        # Таблица просмотренных объявлений — для дедупликации
        await db.execute("""
            CREATE TABLE IF NOT EXISTS seen_listings (
                user_id    INTEGER,
                listing_id TEXT,
                PRIMARY KEY (user_id, listing_id)
            )
        """)
        await db.commit()


async def save_search(user_id, make, model, year_from, year_to, price_max, mileage_max):
    """Сохраняет или обновляет настройки поиска пользователя."""
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
    """Возвращает настройки поиска пользователя или None."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM searches WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def get_all_active_searches():
    """Возвращает список всех пользователей у которых поиск активен."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM searches WHERE is_active = 1"
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def set_active(user_id, active):
    """Включает или выключает поиск."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE searches SET is_active = ? WHERE user_id = ?",
            (1 if active else 0, user_id)
        )
        await db.commit()


async def add_seen_listing(user_id, listing_id) -> bool:
    """
    Добавляет объявление в список просмотренных.
    Возвращает True если объявление НОВОЕ.
    Возвращает False если уже видели раньше.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        try:
            await db.execute(
                "INSERT INTO seen_listings (user_id, listing_id) VALUES (?, ?)",
                (user_id, listing_id)
            )
            await db.commit()
            return True   # Объявление новое!
        except aiosqlite.IntegrityError:
            return False  # Уже видели — пропускаем