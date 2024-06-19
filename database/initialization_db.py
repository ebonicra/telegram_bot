import sqlite3
import json
import random
import os
from players_classes import Protagonist, NPC, Enemy

JSON_DIR = os.path.join(os.path.dirname(__file__), '../jsons')


def create_new_user(user_id: int, user_name: str, db_file: str = 'game.db') -> None:
    """
    Функция создает нового пользователя и сохраняет его в базе данных.
    Параметры:
        user_id (int): Идентификатор пользователя.
        user_name (str): Имя пользователя.
        db_file (str, optional): Имя файла базы данных. По умолчанию 'game.db'.
    """
    new_user = Protagonist(user_id, user_name)
    new_user.save_to_db(db_file)


def create_npc(user_id: int, db_file: str = 'game.db') -> None:
    """
    Функция создает NPC и сохраняет их в базе данных.
    Параметры:
        user_id (int): Идентификатор пользователя.
        db_file (str, optional): Имя файла базы данных. По умолчанию 'game.db'.
    """
    npc_data = load_json_file('npc.json')
    dialogues = load_json_file('dialogues.json')['npc']
    inventory_data = load_json_file('inventory.json')
    alcohol_knowledge = inventory_data['knowledge']
    recipe_knowledge = inventory_data['recipes']
    bartender_knowledge = inventory_data['items']
    quest_knowledge = inventory_data['quest']
    alcohol_knowledge_combinations, other_knowledge_combinations = create_knowledge_combinations(
        alcohol_knowledge, recipe_knowledge, bartender_knowledge, quest_knowledge)

    for i in range(1, 25):
        type_npc, name_npc = random.choice([
            get_random_npc_women(
                npc_data['type_women'], npc_data['name_women']),
            get_random_npc_men(npc_data['type_men'], npc_data['name_men'])
        ])
        location_id = i % 8 + 1
        dialogue = random.choice(dialogues)
        npc_knowledge = assign_knowledge_to_npc(
            alcohol_knowledge_combinations, other_knowledge_combinations)
        dialogue_done = 0
        knowledge_done = 0
        recipe_done = 0
        bartender_done = 0
        quest_done = 0
        new_npc = NPC(
            type_npc, name_npc, location_id, dialogue,
            npc_knowledge['alcohol_knowledge'],
            npc_knowledge['recipe_knowledge'],
            npc_knowledge['bartender_knowledge'],
            npc_knowledge['quest_knowledge'],
            dialogue_done,
            knowledge_done,
            recipe_done,
            bartender_done,
            quest_done,
            user_id
        )
        new_npc.save_to_db(db_file)


def create_enemy(user_id: int, db_file: str = 'game.db') -> None:
    """
    Функция создает врагов (барменов) и сохраняет их в базе данных.
    Параметры:
        user_id (int): Идентификатор пользователя.
        db_file (str, optional): Имя файла базы данных. По умолчанию 'game.db'.
    """
    dialogues = load_json_file('dialogues.json')['enemy']
    Enemy('Бармен-стажер', 'Артур', 1, 1000, 5,
          random.choice(dialogues), 0, user_id).save_to_db(db_file)
    Enemy('Бармен-sex', 'Георгий', 1, 1000, 7,
          random.choice(dialogues), 0, user_id).save_to_db(db_file)
    Enemy('Бармен-казах', 'Рахат', 1, 1000, 10,
          random.choice(dialogues), 0, user_id).save_to_db(db_file)
    Enemy('Бармен-сверхчеловек', 'Фридрих', 6, 1000, 12,
          random.choice(dialogues), 0, user_id).save_to_db(db_file)
    Enemy('Бармен-император', 'Людвиг', 6, 1000, 15,
          random.choice(dialogues), 0, user_id).save_to_db(db_file)


def create_quest(user_id: int, db_file: str = 'game.db') -> None:
    """
    Функция создает квесты и сохраняет их в базе данных.
    Параметры:
        user_id (int): Идентификатор пользователя.
        db_file (str, optional): Имя файла базы данных. По умолчанию 'game.db'.
    """
    quests = [
        {"quest_name": "Quiz", "description": "Ответь на 10 вопросов викторины без ошибок и получи счастье.",
            "count": 0, "done": 0, "user": user_id},
        {"quest_name": "Bar", "description": "Расскажи про 5 барменских штук.",
            "count": 0, "done": 0, "user": user_id},
        {"quest_name": "Photographer", "description": "Сделай 5 селфи.",
            "count": 0, "done": 0, "user": user_id},
        {"quest_name": "Recipe", "description": "Расскажи рецепт Негрони.",
            "count": 0, "done": 0, "user": user_id},
        {"quest_name": "Cigarette", "description": "Угости по-братски сигареткой.",
            "count": 0, "done": 0, "user": user_id},
        {"quest_name": "Selfie", "description": "Хочешь сделать селфи?",
            "count": 0, "done": 0, "user": user_id},
        {"quest_name": "Roof", "description": "Хочешь спрыгнуть с крыши?",
            "count": 0, "done": 0, "user": user_id},
        {"quest_name": "Bartenders", "description": "Сколько барменов ты уже перепил?",
            "count": 0, "done": 0, "user": user_id}
    ]
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.executemany('''INSERT INTO quest (quest_name, description, count, done, user) 
                              VALUES (:quest_name, :description, :count, :done, :user)''', quests)
        conn.commit()


def create_knowledge_combinations(alcohol_knowledge: list, recipe_knowledge: list, bartender_knowledge: list, quest_knowledge: list) -> tuple:
    """
    Функция создает комбинации знаний для NPC.
    Параметры:
        alcohol_knowledge (list): Список знаний о видах алкоголя.
        recipe_knowledge (list): Список знаний о рецептах коктейлей.
        bartender_knowledge (list): Список знаний о барменских штуках.
        quest_knowledge (list): Список знаний о квестах.
    Возвращает:
        tuple: Кортеж из двух списков:
            - alcohol_knowledge_combinations: Комбинации знаний о видах алкоголя.
            - other_knowledge_combinations: Комбинации других знаний (рецепты, барменские штуки, квесты).
    """
    random.shuffle(alcohol_knowledge)
    random.shuffle(recipe_knowledge)
    random.shuffle(bartender_knowledge)
    random.shuffle(quest_knowledge)

    alcohol_knowledge_combinations = [
        (item, 'alcohol_knowledge') for item in alcohol_knowledge[:24]]
    other_knowledge_combinations = [
        (item, 'recipe_knowledge') for item in recipe_knowledge[:12]
    ] + [
        (item, 'bartender_knowledge') for item in bartender_knowledge[:7]
    ] + [
        (item, 'quest_knowledge') for item in quest_knowledge[:5]
    ]
    random.shuffle(other_knowledge_combinations)
    return alcohol_knowledge_combinations, other_knowledge_combinations


def assign_knowledge_to_npc(alcohol_knowledge_combinations: list, other_knowledge_combinations: list) -> dict:
    """
    Функция назначает знания NPC из созданных комбинаций.
    Параметры:
        alcohol_knowledge_combinations (list): Список комбинаций знаний о видах алкоголя.
        other_knowledge_combinations (list): Список комбинаций других знаний (рецепты, барменские штуки, квесты).
    Возвращает:
        dict: Словарь с назначенными знаниями NPC.
    """
    npc_knowledge = {
        'alcohol_knowledge': None,
        'recipe_knowledge': None,
        'bartender_knowledge': None,
        'quest_knowledge': None
    }
    alcohol_knowledge = alcohol_knowledge_combinations.pop()
    other_knowledge = other_knowledge_combinations.pop()
    npc_knowledge[alcohol_knowledge[1]] = alcohol_knowledge[0]
    npc_knowledge[other_knowledge[1]] = other_knowledge[0]
    return npc_knowledge


def load_json_file(filename: str) -> dict:
    """
    Функция загружает данные из JSON файла.
    Параметры:
        filename (str): Имя JSON файла.
    Возвращает:
        dict: Данные из JSON файла в виде словаря.
    """
    with open(os.path.join(JSON_DIR, filename), 'r', encoding='utf-8') as file:
        return json.load(file)


def get_random_npc_women(type_women: list, name_women: list) -> tuple:
    """
    Функция возвращает случайного NPC женского пола.
    Параметры:
        type_women (list): Список типов NPC женского пола.
        name_women (list): Список имен NPC женского пола.
    Возвращает:
        tuple: Кортеж из типа и имени NPC женского пола.
    """
    return random.choice(type_women), random.choice(name_women)


def get_random_npc_men(type_men: list, name_men: list) -> tuple:
    """
    Функция возвращает случайного NPC мужского пола.
    Параметры:
        type_men (list): Список типов NPC мужского пола.
        name_men (list): Список имен NPC мужского пола.
    Возвращает:
        tuple: Кортеж из типа и имени NPC мужского пола.
    """
    return random.choice(type_men), random.choice(name_men)
