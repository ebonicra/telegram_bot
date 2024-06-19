import sqlite3


def data_create_tables() -> None:
    """
    Создает таблицы в базе данных 'game.db', если они не существуют.
    Таблицы:
    - users: содержит информацию о пользователях.
    - npc: содержит информацию о неигровых персонажах.
    - enemy: содержит информацию о врагах.
    """
    with sqlite3.connect('game.db') as conn:
        cursor = conn.cursor()

        # Создание таблицы users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                current_location_id INTEGER,
                money INTEGER DEFAULT 100,
                intoxication_level INTEGER DEFAULT 1000,
                knowledge INTEGER DEFAULT 0,
                alcohol_knowledge TEXT DEFAULT '{}',
                cocktail_recipes TEXT DEFAULT '{}',
                bartender_items TEXT DEFAULT '{}',
                other_items TEXT DEFAULT '{}',
                FOREIGN KEY (current_location_id) REFERENCES locations (id)
            )
        ''')

        # Создание таблицы npc
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS npc (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                location_id INTEGER,
                dialogue TEXT,
                knowledge_info TEXT,
                recipe_info TEXT,
                bartender_info TEXT,
                quest TEXT,
                dialogue_done INTEGER DEFAULT 0,
                knowledge_done INTEGER DEFAULT 0,
                recipe_done INTEGER DEFAULT 0,
                bartender_done INTEGER DEFAULT 0,
                quest_done INTEGER DEFAULT 0,
                user INTEGER NOT NULL,
                FOREIGN KEY (location_id) REFERENCES locations (id),
                FOREIGN KEY (user) REFERENCES users (user_id)
            )
        ''')

        # Создание таблицы enemy
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enemy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                location_id INTEGER,
                intoxication_level INTEGER,
                knowledge INTEGER,
                dialogue TEXT,
                defeated INTEGER NOT NULL DEFAULT 0,
                user INTEGER NOT NULL,
                FOREIGN KEY (location_id) REFERENCES locations (id),
                FOREIGN KEY (user) REFERENCES users (user_id)
            )
        ''')
        conn.commit()
