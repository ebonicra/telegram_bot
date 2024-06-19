import sqlite3


def map_create_tables() -> None:
    """
    Создает таблицы, загружает локации и пути в базу данных 'game.db'.
    """
    with sqlite3.connect('game.db') as conn:
        create_tables()
        load_locations()
        load_paths()


def create_tables() -> None:
    """
    Создает таблицы в базе данных 'game.db', если они не существуют.
    Таблицы:
    - locations: содержит информацию о локациях.
    - paths: содержит информацию о путях между локациями.
    """
    with sqlite3.connect('game.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            song TEXT NOT NULL,
            smell TEXT NOT NULL,
            image TEXT NOT NULL,
            is_start BOOLEAN NOT NULL DEFAULT 0
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_location_id INTEGER NOT NULL,
            to_location_id INTEGER NOT NULL,
            direction TEXT NOT NULL,
            FOREIGN KEY (from_location_id) REFERENCES locations (id),
            FOREIGN KEY (to_location_id) REFERENCES locations (id)
        )''')

        conn.commit()


def load_locations() -> None:
    """
    Загружает предопределенные локации в базу данных.
    """
    locations = [
        ("Бар", "Это ваш центр культурного выпивания. Тут хочется простого человеческого \"отстаньте от меня, я отдыхаю\".",
         "Jazz in Paris", "Ароматы виски и пива вместе с запахом сочного стейка, который заказал мужик за соседним столиком", "images/locations/bar.jpeg", True),
        ("Курилка", "Лучшее место, чтоб надышаться табачком и послушать интересные истории.",
         "Smoke on the Water", "Запах вейперов этих вездесущих.", "images/locations/smoking_room.jpeg", False),
        ("Улица", "Лучшее место, чтоб подышать воздухом, посмотреть на небо и преисполниться вселенской благодати, пока тебя не нашли друзья, от которых ты сбежал.",
         "Street Life", "Аромат свежести, свободы и автомобильных выхлопов.", "images/locations/street.jpeg", False),
        ("Туалет", "Место, где можно спрятаться, если ты очень пьяный, и заснуть в кабинке. А вообще это лучшее место, чтоб привести себя в порядок.",
         "Quiet Bathroom Ambience", "Лучше не знать, чем тут пахнет.", "images/locations/bathroom.jpeg", False),
        ("Танцпол", "Место, куда ты сбежишь, чтоб оттанцевать все свои проблемы и потерется попками с незнакомыми людьми. Однако данной возможностью пользуются только очень смелые или очень тупые.",
         "Stayin' Alive", "Аромат пота и вонючих сладких духов от малолеток.", "images/locations/dance_floor.jpeg", False),
        ("Бар на крыше", "Место, где красиво и вкусно. Тут можно словить самый большой релакс, пить приятные напитки, ни с кем не разговаривать и смотерть на город.",
         "Moon River", "Свежий аромат ночный звезд и тишины.", "images/locations/rooftop_bar.jpeg", False),
        ("Коридор", "Самое грязное, но вместе с тем популярное место. Сюда идут люди, чтоб пообжиматься с друг другом, как-будто их никто не видит.",
         "Corridor Echo", "Запах тесноты, пота и невинной молодости.", "images/locations/hall_bar.jpeg", False),
        ("Ночной ларек", "Небольшой ночной ларек, расположенный неподалеку от бара. Здесь можно купить какую-нибудь ерунду в память об этом вечере.",
         "Night Market", "Аромат свежей смайков и дешевых шоколадок.", "images/locations/night_market.jpeg", False)
    ]
    for location in locations:
        create_location(location)


def create_location(location: tuple[str, str, str, str, str, bool]) -> int:
    """
    Добавляет новую локацию в базу данных.

    :param location: Кортеж с данными о локации (name, description, song, smell, image, is_start).
    :return: ID созданной локации.
    """
    with sqlite3.connect('game.db') as conn:
        sql = '''INSERT INTO locations(name, description, song, smell, image, is_start)
                 VALUES(?,?,?,?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, location)
        conn.commit()
        return cur.lastrowid


def load_paths() -> None:
    """
    Загружает предопределенные пути в базу данных.
    """
    paths = [
        (1, 3, 'down'),
        (1, 5, 'left'),
        (1, 4, 'right'),
        (1, 7, 'up'),
        (2, 4, 'down'),
        (2, 7, 'right'),
        (3, 1, 'up'),
        (3, 8, 'left'),
        (4, 1, 'left'),
        (4, 2, 'up'),
        (5, 1, 'right'),
        (6, 7, 'down'),
        (7, 6, 'up'),
        (7, 2, 'right'),
        (7, 1, 'down'),
        (8, 3, 'left')
    ]
    for path in paths:
        create_path(path)


def create_path(path: tuple[int, int, str]) -> int:
    """
    Добавляет новый путь в базу данных.

    :param path: Кортеж с данными о пути (from_location_id, to_location_id, direction).
    :return: ID созданного пути.
    """
    with sqlite3.connect('game.db') as conn:
        sql = '''INSERT INTO paths(from_location_id, to_location_id, direction)
                 VALUES(?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, path)
        conn.commit()
        return cur.lastrowid
