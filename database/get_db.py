import sqlite3
import json
from typing import Union

from players_classes import NPC, Enemy

# Множество допустимых столбцов для запросов
VALID_COLUMNS = {'id', 'user_id', 'type', 'name', 'current_location_id', 'money', 'intoxication_level',
                 'knowledge', 'alcohol_knowledge', 'cocktail_recipes', 'bartender_items', 'other_items'}

# Множество столбцов, содержащих данные в формате JSON
JSON_COLUMNS = {'alcohol_knowledge', 'cocktail_recipes',
                'bartender_items', 'other_items'}


def get_user_data(item: str, user_id: int, db_file: str = 'game.db') -> Union[str, dict, int, None]:
    """
    Функция для получения данных пользователя из базы данных.
    Параметры:
    - item (str): Название столбца, данные которого необходимо извлечь.
    - user_id (int): Идентификатор пользователя, чьи данные нужно получить.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    Возвращает:
    - Union[str, dict, int, None]: Данные указанного столбца. Если данные содержатся в формате JSON, возвращается декодированный JSON. Если данных нет, возвращается None.
    Выбрасывает:
    - ValueError: Если указан недопустимый столбец (не входит в VALID_COLUMNS).
    - ValueError: Если данные в столбце JSON не удалось декодировать.
    """
    if item not in VALID_COLUMNS:
        raise ValueError(f"Invalid column name: {item}")
    query = f"SELECT {item} FROM users WHERE user_id = ?"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result:
            data = result[0]
            if item in JSON_COLUMNS:
                try:
                    return json.loads(data)
                except json.JSONDecodeError:
                    raise ValueError(f"Data for {item} is not valid JSON.")
            return data
        return None


def get_path_data(location_id: int, db_file: str = 'game.db') -> list[tuple[int, str]]:
    """
    Функция для получения данных о доступных путях из указанной локации.
    Параметры:
    - location_id (int): Идентификатор начальной локации.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    Возвращает:
    - list[tuple[int, str]]: Список кортежей, содержащих идентификаторы конечных локаций и направления путей.
    """
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT to_location_id, direction FROM paths WHERE from_location_id = ?', (location_id,))
        directions = cursor.fetchall()
        return directions


def get_location_data(item: str, location_id: int, db_file: str = 'game.db') -> str:
    """
    Функция для получения данных о указанной локации из базы данных.
    Параметры:
    - item (str): Название столбца, данные которого необходимо извлечь.
    - location_id (int): Идентификатор локации, данные о которой нужно получить.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    Возвращает:
    - str: Значение указанного столбца для указанной локации.
    """
    query = f"SELECT {item} FROM locations WHERE id = ?"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (location_id,))
        return cursor.fetchone()[0]


async def get_npc_list(location_id: int, user_id: int, db_file: str = 'game.db') -> list[tuple[int, str, str]]:
    """
    Функция для получения списка NPC в указанной локации для указанного пользователя.
    Параметры:
    - location_id (int): Идентификатор локации, в которой находятся NPC.
    - user_id (int): Идентификатор пользователя, для которого нужно получить NPC.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    Возвращает:
    - List[Tuple[int, str, str]]: Список кортежей, содержащих идентификатор NPC, их тип и имя.
    """
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, type, name FROM npc WHERE location_id = ? and user = ?", (location_id, user_id))
        return cursor.fetchall()


def get_npc_info(npc_id: int, db_file: str = 'game.db') -> NPC:
    """
    Функция для получения подробной информации о NPC по его идентификатору.
    Параметры:
    - npc_id (int): Идентификатор NPC, информацию о котором нужно получить.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    Возвращает:
    - NPC: Объект NPC, содержащий подробную информацию.
    """
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT type, name, location_id, dialogue, knowledge_info, recipe_info, bartender_info, quest, dialogue_done, knowledge_done, recipe_done, bartender_done, quest_done, user FROM npc WHERE id = ?", (npc_id,))
        npc_info = cursor.fetchone()
        npc = NPC(*npc_info)
    return npc


def get_npc_data(user_id: int, quest_name: str, db_file: str = 'game.db') -> int:
    """
    Функция для получения НПС согласно его квесту.
    Параметры:
    - user_id (int): Идентификатор пользователя.
    - quest_name (str): Название квеста.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    Возвращает:
    - npc_id: Идентификатор НПС, у которого соответствует пользователя и название квеста.
    """
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM npc WHERE user = ? and quest = ?", (user_id, quest_name))
        npc_id = cursor.fetchone()[0]
    return npc_id


async def get_enemy_list(location_id: int, user_id: int, db_file: str = 'game.db') -> list[tuple[int, str, str, int]]:
    """
    Функция для получения списка врагов (Enemy) в указанной локации для указанного пользователя.
    Параметры:
    - location_id (int): Идентификатор локации, в которой находятся враги.
    - user_id (int): Идентификатор пользователя, для которого нужно получить врагов.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    Возвращает:
    - list[tuple[int, str, str, int]]: Список кортежей, содержащих идентификатор врага, их тип, имя и статус (побежден или нет).
    """
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, type, name, defeated FROM enemy WHERE location_id = ? and user = ?", (location_id, user_id))
        return cursor.fetchall()


def get_enemy_info(enemy_id: int, db_file: str = 'game.db') -> Enemy:
    """
    Функция для получения подробной информации о враге (Enemy) по его идентификатору.
    Параметры:
    - enemy_id (int): Идентификатор врага, информацию о котором нужно получить.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    Возвращает:
    - Enemy: Объект Enemy, содержащий подробную информацию.
    """
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT type, name, location_id, intoxication_level, knowledge, dialogue, defeated, user FROM enemy WHERE id = ?", (enemy_id,))
        enemy_info = cursor.fetchone()
        enemy = Enemy(*enemy_info)
    return enemy


def get_count_defeated_enemy(user_id: int, db_file: str = 'game.db') -> int:
    """
    Функция для получения количества побежденных врагов пользователя по его идентификатору.
    Параметры:
    - user_id (int): Идентификатор пользователя, для которого нужно получить количество побежденных врагов.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    Возвращает:
    - int: Количество побежденных врагов пользователя.
    """
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT count FROM quest WHERE quest_name = ? and user = ?', ('Bartenders', user_id))
        return cursor.fetchone()[0]


def get_quest_data(item: str, quest_name: str, user_id: int, db_file: str = 'game.db') -> Union[str, int, None]:
    """
    Функция для получения данных о квесте для указанного пользователя.
    Параметры:
    - item (str): Название столбца, данные которого необходимо извлечь.
    - quest_name (str): Название квеста, данные о котором нужно получить.
    - user_id (int): Идентификатор пользователя, для которого нужно получить данные о квесте.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    Возвращает:
    - Union[str, int, None]: Данные указанного столбца квеста. Возвращается None, если данных нет.
    """
    query = f"SELECT {item} FROM quest WHERE quest_name = ? and user = ?"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (quest_name, user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


def update_user_data(item: str, value: Union[str, int], user_id: int, db_file: str = 'game.db') -> None:
    """
    Функция для обновления данных пользователя в базе данных.
    Параметры:
    - item (str): Название столбца, данные которого необходимо обновить.
    - value (Union[str, int]): Новое значение для указанного столбца.
    - user_id (int): Идентификатор пользователя, чьи данные нужно обновить.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    Выбрасывает:
    - ValueError: Если указан недопустимый столбец (не входит в VALID_COLUMNS).
    - ValueError: Если значение для столбца JSON невозможно сериализовать в формат JSON.
    """
    if item not in VALID_COLUMNS:
        raise ValueError(f"Invalid column name: {item}")
    if item in JSON_COLUMNS:
        try:
            value = json.dumps(value, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            raise ValueError(
                f"Provided value for {item} is not valid JSON. {e}")
    query = f"UPDATE users SET {item} = ? WHERE user_id = ?"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (value, user_id,))
        conn.commit()


def update_quest_data(item: str, value: Union[str, int], quest_name: str, user_id: int, db_file: str = 'game.db') -> None:
    """
    Функция для обновления данных квеста в базе данных.
    Параметры:
    - item (str): Название столбца, данные которого необходимо обновить.
    - value (Union[str, int]): Новое значение для указанного столбца.
    - quest_name (str): Название квеста, данные о котором нужно обновить.
    - user_id (int): Идентификатор пользователя, для которого нужно обновить данные о квесте.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    """
    query = f"UPDATE quest SET {item} = ? WHERE quest_name = ? and user = ?"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (value, quest_name, user_id,))
        conn.commit()


def update_enemy_data(item: str, value: Union[str, int], enemy_name: str, user_id: int, db_file: str = 'game.db') -> None:
    """
    Функция для обновления данных врага (Enemy) в базе данных.
    Параметры:
    - item (str): Название столбца, данные которого необходимо обновить.
    - value (Union[str, int]): Новое значение для указанного столбца.
    - enemy_name (str): Имя врага, данные о котором нужно обновить.
    - user_id (int): Идентификатор пользователя, для которого нужно обновить данные о враге.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    """
    query = f"UPDATE enemy SET {item} = ? WHERE name = ? and user = ?"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (value, enemy_name, user_id,))
        conn.commit()


def update_npc_data(item: str, value: int, npc_id: int, db_file: str = 'game.db') -> None:
    """
    Функция для обновления данных NPC в базе данных.
    Параметры:
    - item (str): Название столбца, данные которого необходимо обновить.
    - value (int): Новое значение для указанного столбца.
    - npc_id (int): Идентификатор NPC, для которого нужно обновить данные.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    """
    query = f"UPDATE npc SET {item} = ? WHERE id = ?"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (value, npc_id,))
        conn.commit()


def reset_user_data(user_id: int, db_file: str = 'game.db') -> None:
    """
    Функция для сброса данных пользователя из базы данных.
    Параметры:
    - user_id (int): Идентификатор пользователя, чьи данные нужно сбросить.
    - db_file (str): Путь к файлу базы данных (по умолчанию 'game.db').
    """
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM npc WHERE user = ?', (user_id,))
        cursor.execute('DELETE FROM quest WHERE user = ?', (user_id,))
        cursor.execute('DELETE FROM enemy WHERE user = ?', (user_id,))
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()
