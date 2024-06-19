from collections import defaultdict
import json
import sqlite3

INTOXICATION = {
    0: "белочек",
    1: "белочку",
    2: "белочки",
    3: "белочки",
    4: "белочки",
    5: "белочек",
    6: "белочек",
    7: "белочек",
    8: "белочек",
    9: "белочек",
    10: "белочек",
    11: "белочек",
    12: "белочек",
    13: "белочек",
    14: "белочек",
    15: "белочек"
}

SHOT = {
    1: "шот",
    2: "шота",
    3: "шота",
    4: "шота",
    5: "шотов",
    6: "шотов"
}


class Protagonist:
    def __init__(self, user_id: str, name: str):
        """
        Инициализация объекта Протагониста (Улитки).
        Параметры:
        - user_id: идентификатор пользователя (строка).
        - name: имя пользователя (строка).
        """
        self.id = user_id
        self.type = "Улитка"
        self.name = name
        self.current_location_id = 1
        self.money = 2000
        self.intoxication_level = 1000
        self.knowledge = 0
        self.alcohol_knowledge = defaultdict(str)
        self.cocktail_recipes = defaultdict(str)
        self.bartender_items = defaultdict(str)
        self.other_items = defaultdict(str)

    def save_to_db(self, db_file: str = 'game.db') -> None:
        """
        Сохранение информации о пользователе в базу данных.
        Параметры:
        - db_file: имя файла базы данных (строка).
        """
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_id, type, name, current_location_id, money, intoxication_level, knowledge, alcohol_knowledge, cocktail_recipes, bartender_items, other_items) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (self.id, self.type, self.name, self.current_location_id, self.money, self.intoxication_level, self.knowledge, json.dumps(self.alcohol_knowledge), json.dumps(self.cocktail_recipes), json.dumps(self.bartender_items), json.dumps(self.other_items)))
            conn.commit()

    def whoami(self, db_file: str = 'game.db') -> str:
        """
        Получение информации о пользователе из базы данных.
        Параметры:
        - db_file: имя файла базы данных (строка).
        Возвращает:
        - Строка с информацией о пользователе.
        """
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, money, intoxication_level, knowledge FROM users WHERE user_id = ?", (self.id,))
            user = cursor.fetchone()
        if user:
            name, money, intoxication_level, knowledge = user
            intoxication_level = intoxication_level // 1000
            intoxication = INTOXICATION.get(intoxication_level)
            return (f"🐌 Характеристики вашего героя 🐌\n\n"
                    f"Дорогая улиточка, тебя зовут {name}, уже все свои улиточные мозги пропила, раз имя забываешь.\n"
                    f"Пьяна ты уже на {intoxication_level} {intoxication} из 10\n"
                    f"Money for drink осталось всего {money}$\n"
                    f"Твой уровень айкью равен {knowledge}")
        else:
            return "Такой улитки не существует. Что-то пошло не так"

    def whereami(self) -> tuple:
        """
        Получение информации о текущей локации пользователя из базы данных.
        Возвращает:
        - Кортеж с изображением и описанием текущей локации.
        """
        with sqlite3.connect('game.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT current_location_id FROM users WHERE user_id = ?', (self.id,))
            location_id = cursor.fetchone()[0]
            self.current_location_id = location_id
            cursor.execute(
                'SELECT name, description, song, smell, image FROM locations WHERE id = ?', (location_id,))
            location = cursor.fetchone()
            name, description, song, smell, image = location
            return image, (f"Локация: {name}\n"
                           f"Описание: {description}\n"
                           f"Музыка: {song}\n"
                           f"Аромат: {smell}\n")

    def go(self, new_location_id: int) -> None:
        """
        Изменение текущей локации пользователя в базе данных.
        Параметры:
        - new_location_id: новый ID локации (целое число).
        """
        with sqlite3.connect('game.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET current_location_id = ? WHERE user_id = ?', (new_location_id, self.id))

    def send_inventory(self) -> bool:
        """
        Отправка инвентаря пользователя.
        Получает информацию из базы данных о знаниях, рецептах, предметах и других предметах пользователя.
        Возвращает:
        - True, если информация о пользователе получена успешно, иначе False.
        """
        with sqlite3.connect('game.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT alcohol_knowledge, cocktail_recipes, bartender_items, other_items FROM users WHERE user_id = ?', (self.id,))
            user_data = cursor.fetchone()
            if user_data:
                alcohol_knowledge, cocktail_recipes, bartender_items, other_items = user_data
                self.alcohol_knowledge = json.loads(alcohol_knowledge)
                self.cocktail_recipes = json.loads(cocktail_recipes)
                self.bartender_items = json.loads(bartender_items)
                self.other_items = json.loads(other_items)
                return True
            else:
                return False

    def send_inventory_type(self, type_inventory: str) -> list:
        """
        Отправка определённого типа инвентаря пользователя.
        Параметры:
        - type_inventory: тип инвентаря ('knowledge', 'recipes', 'items', 'other').
        Возвращает:
        - Список строк с информацией о предметах указанного типа.
        """
        inventory_map = {
            'knowledge': ('алкогольные знания', self.alcohol_knowledge, "🍾"),
            'recipes': ('рецепты коктейлей', self.cocktail_recipes, "🍹"),
            'items': ('барменские штуки', self.bartender_items, "🫗"),
            'other': ('приколы, которые мы купили', self.other_items, "🤡"),
        }
        title, inventory, emoji = inventory_map.get(
            type_inventory, ('', {}, ''))
        if not inventory:
            return [f"А нет, нету у тебя никаких знаний в {title}. Понимаешь? НИ КА КИХ"]
        response = [f"\n{title.capitalize()}:\n"]
        for k, v in inventory.items():
            if type_inventory == 'other':
                response.append(f"{emoji} {k} в количестве {v} шт\n")
            else:
                response.append(f"{emoji} {k}: {v}\n")
        return response

    def drink(self, snail_roll: int) -> list:
        """
        Процесс употребления алкоголя пользователем.
        Параметры:
        - snail_roll: результат броска кубика (целое число).
        Возвращает:
        - Список строк с информацией о процессе употребления алкоголя.
        """
        with sqlite3.connect('game.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT intoxication_level, knowledge FROM users WHERE user_id = ?', (self.id,))
            user_data = cursor.fetchone()
            if not user_data:
                return "Такой улитки не существует. Что-то пошло не так"
            self.intoxication_level, self.knowledge = user_data

        response = []
        snail_loss = snail_roll * 1000 - self.knowledge * 50
        if snail_loss < 0:
            snail_loss = 0

        shot = SHOT.get(snail_roll)
        response.append(f"😍 Let's drink 😍\nТы должен выпить {snail_roll} {shot}.")
        response.append(
            f"Урон твоей нежной печени состовляет {snail_loss} феечек вич.")

        self.intoxication_level += snail_loss
        avaliable_level = 10 - (self.intoxication_level // 1000)
        if self.intoxication_level >= 10000:
            response.append(
                "Малышка - ты напилась.\nХорошо хоть, что ты улитка и у тебя нет ног, иначе бы уже свалилась.")
            response.append(
                "Советую навестить своего белого друга в уборной и чуть протрезветь, чтоб ещё надрать задницы этим барменам.")
        else:
            response.append("Не умерла и слава улиточному богу.")
            response.append(
                f"Но учти, до твоего опьянения осталось {avaliable_level} уровней кайфа.")
        with sqlite3.connect('game.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET intoxication_level = ? WHERE user_id = ?',
                           (self.intoxication_level, self.id))
            conn.commit()
        return response


class NPC:
    def __init__(self, type: str, name: str, location_id: int, dialogue: str, knowledge_info: str, recipe_info: str, bartender_info: str, quest: str, dialogue_done: int,  knowledge_done: int, recipe_done: int, bartender_done: int, quest_done: int, user: int):
        """
        Инициализация объекта NPC.
        Параметры:
        - type: тип NPC (строка).
        - name: имя NPC (строка).
        - location_id: ID локации NPC (целое число).
        - dialogue: диалог NPC (строка).
        - knowledge_info: информация о знании, которое NPC может поделиться (строка в формате "название-описание").
        - recipe_info: информация о рецепте, который NPC может поделиться (строка в формате "название-описание").
        - bartender_info: информация о предмете, который NPC может поделиться (строка в формате "название-описание").
        - quest: информация о квесте NPC (строка).
        - dialogue_done: индикатор рассказа диалога.
        - knowledge_done: индикатор рассказа алкогольного знания.
        - recipe_done: индикатор рассказа рецепта.
        - bartender_done: индикатор рассказа о барменском предмете.
        - quest_done: индикатор выполнения квеста.
        - user: ID пользователя (целое число).
        """
        self.type = type
        self.name = name
        self.location_id = location_id
        self.dialogue = dialogue
        self.knowledge_info = knowledge_info
        self.recipe_info = recipe_info
        self.bartender_info = bartender_info
        self.quest = quest
        self.dialogue_done = dialogue_done
        self.knowledge_done = knowledge_done
        self.recipe_done = recipe_done
        self.bartender_done = bartender_done
        self.quest_done = quest_done
        self.user = user

    def save_to_db(self, db_file: str = 'game.db') -> None:
        """
        Сохраняет информацию о NPC в базу данных.
        Параметры:
        - db_file: имя файла базы данных (строка).
        """
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO npc (type, name, location_id, dialogue, knowledge_info, recipe_info, bartender_info, quest, user) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (self.type, self.name, self.location_id, self.dialogue, self.knowledge_info, self.recipe_info, self.bartender_info, self.quest, self.user))
            conn.commit()

    def share_knowledge(self):
        """
        Функция, чтоб поделиться знанием от НПС с пользователем.
        Возвращает:
        - Строка с информацией о знании.
        """
        with sqlite3.connect('game.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT knowledge, alcohol_knowledge FROM users WHERE user_id = ?', (self.user,))
            user_data = cursor.fetchone()
            if not user_data:
                return "Такой улитки не существует. Что-то пошло не так"
            knowledge, alcohol_knowledge_json = user_data
            alcohol_knowledge = json.loads(alcohol_knowledge_json)
            alco, alco_description = self.knowledge_info.split('-')
            if alco in alcohol_knowledge:
                return f"I'm so sorry, но ты тупица, я тебе уже рассказывал, что такое {alco.lower()}"
            else:
                alcohol_knowledge[alco] = alco_description
                cursor.execute(
                    'UPDATE users SET knowledge = ?, alcohol_knowledge = ? WHERE user_id = ?',
                    (knowledge + 1, json.dumps(alcohol_knowledge,
                     ensure_ascii=False), self.user)
                )
                conn.commit()
                return f"{alco} - {alco_description}"

    def share_recipe(self):
        """
        Функция, чтоб поделиться рецептом от НПС с пользователем.
        Возвращает:
        - Строка с информацией о знании.
        """
        with sqlite3.connect('game.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT knowledge, cocktail_recipes FROM users WHERE user_id = ?', (self.user,))
            user_data = cursor.fetchone()
            if not user_data:
                return "Такой улитки не существует. Что-то пошло не так"
            knowledge, cocktail_recipes_json = user_data
            cocktail_recipes = json.loads(cocktail_recipes_json)
            recipe, recipe_description = self.recipe_info.split('-')
            if recipe in cocktail_recipes:
                return f"Оуу, ты же уже знаешь {recipe.lower()}, вопрос в другом, приготовишь ли ты его хоть раз в жизни?"
            else:
                cocktail_recipes[recipe] = recipe_description
                cursor.execute(
                    'UPDATE users SET knowledge = ?, cocktail_recipes = ? WHERE user_id = ?',
                    (knowledge + 1, json.dumps(cocktail_recipes,
                     ensure_ascii=False), self.user)
                )
                conn.commit()
                return f"{recipe} - {recipe_description}"

    def share_item(self):
        """
        Функция, чтоб поделиться барменским предметом от НПС с пользователем.
        Возвращает:
        - Строка с информацией о знании.
        """
        with sqlite3.connect('game.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT knowledge, bartender_items FROM users WHERE user_id = ?', (self.user,))
            user_data = cursor.fetchone()
            if not user_data:
                return "Такой улитки не существует. Что-то пошло не так"
            knowledge, bartender_items_json = user_data
            bartender_items = json.loads(bartender_items_json)
            item, item_description = self.bartender_info.split('-')
            if item in bartender_items:
                return f"Не, зай, {item.lower()} у тебя уже есть. Иди, гуляй."
            else:
                bartender_items[item] = item_description
                cursor.execute(
                    'UPDATE users SET knowledge = ?, bartender_items = ? WHERE user_id = ?',
                    (knowledge + 1, json.dumps(bartender_items,
                     ensure_ascii=False), self.user)
                )
                conn.commit()
                return f"{item} - {item_description}"


class Enemy:
    def __init__(self, type: str, name: str, location_id: int, intoxication_level: int, knowledge: int, dialogue: str, defeated: int, user: int):
        """
        Инициализация объекта Enemy.
        Параметры:
        - type: тип врага (строка).
        - name: имя врага (строка).
        - location_id: ID локации врага (целое число).
        - intoxication_level: уровень опьянения врага (целое число).
        - knowledge: уровень знаний врага (целое число).
        - dialogue: диалог врага (строка).
        - defeated: флаг поражения врага (целое число, 0 или 1).
        - user: ID пользователя (целое число).
        """
        self.type = type
        self.name = name
        self.location_id = location_id
        self.intoxication_level = intoxication_level
        self.knowledge = knowledge
        self.dialogue = dialogue
        self.defeated = defeated
        self.user = user

    def save_to_db(self, db_file: str = 'game.db') -> None:
        """
        Сохраняет информацию о враге в базу данных.
        Параметры:
        - db_file: имя файла базы данных (строка).
        """
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO enemy (type, name, location_id, intoxication_level, knowledge, dialogue, defeated, user) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (self.type, self.name, self.location_id, self.intoxication_level, self.knowledge, self.dialogue, self.defeated, self.user))
            conn.commit()

    def whoisenemy(self) -> str:
        """
        Возвращает информацию о враге.
        Возвращает:
        - Строка с описанием врага.
        """
        intoxication_level = self.intoxication_level // 1000
        intoxication = INTOXICATION.get(intoxication_level)
        return (f"Позвольте представиться, я {self.type.lower()} {self.name}\n"
                f"Моя сила, моя мудрость, мои барменские знания составляют - {self.knowledge} айкью хромосом\n"
                f"Я уже напился на {intoxication_level} {intoxication} из 10\n\n"
                "И да, я пью на рабочем месте, и чё ты мне сделаешь?\n")

    def drink(self, enemy_roll: int, count_defeated: int) -> tuple:
        """
        Обработка напития врагом.
        Параметры:
        - enemy_roll: результат броска кубика врага (целое число).
        - count_defeated: количество побежденных врагов (целое число).
        Возвращает:
        - Кортеж из списка ответов (строки) и флага завершения (True или False).
        """
        enemy_loss = enemy_roll * 1000 - self.knowledge * 50
        response = []
        shot = SHOT.get(enemy_roll)
        response.append(
            f"{self.type} {self.name} должен выпить {enemy_roll} {shot}.")
        response.append(f"Урон его печени состовляет {enemy_loss} феечек вич.")
        self.intoxication_level += enemy_loss
        intoxication_level = self.intoxication_level // 1000
        intoxication = INTOXICATION.get(intoxication_level)
        finish = False
        with sqlite3.connect('game.db') as conn:
            cursor = conn.cursor()
            if self.intoxication_level >= 10000:
                self.defeated = 1
                response.append(
                    f"🎉 Бармен {self.name} пьян в зюзю, ты перепил его! 🎉\n\nТы прям машина по переработке алкоголя.")
                cursor.execute('UPDATE quest SET count = ? WHERE quest_name = ? and user = ?', (
                    count_defeated + 1, 'Bartenders', self.user))
                if count_defeated + 1 == 5:
                    finish = True
            else:
                response.append("Не повезло, не фартануло, не перепил.")
                response.append(
                    f"Этот черт теперь пьян на {intoxication_level} {intoxication} из 10 чебурашечьих.")
            cursor.execute('UPDATE enemy SET intoxication_level = ?, defeated = ? WHERE name = ? and user = ?',
                           (self.intoxication_level, self.defeated, self.name, self.user))
            conn.commit()
        return response, finish
