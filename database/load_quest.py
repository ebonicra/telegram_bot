import sqlite3


def quest_create_tables() -> None:
    """
    Создает таблицу в базе данных 'game.db', если они не существуют.
    Таблица: 
    - quest: содержит информацию о квестах.
    """
    with sqlite3.connect('game.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quest (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quest_name TEXT,
                description TEXT,
                count INTEGER DEFAULT 0,
                done INTEGER DEFAULT 0,
                user INTEGER NOT NULL,
                FOREIGN KEY (user) REFERENCES users (user_id)
            )
        ''')
        conn.commit()
