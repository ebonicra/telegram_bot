import time
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random

from players_classes import NPC
from database.get_db import get_npc_info, update_npc_data
from handlers import quest
from . import main_buttons

# Constants for defeated enemies
DEFEATED_ENEMY = {
    0: "🧛‍♂️",
    1: "☠️"
}

READ_NPC = {
    0: "❓",
    1: "❔"
}


async def create_character_keyboard(npc_list: list, enemy_list: list) -> InlineKeyboardBuilder:
    """
    Создает клавиатуру для выбора персонажей и врагов.
    Параметры:
    - npc_list: Список NPC (id, type, name).
    - enemy_list: Список врагов (id, type, name, defeated).
    Возвращает:
    - InlineKeyboardBuilder: Построенную клавиатуру.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="❌ Не хочу с ними говорить ❌", callback_data=f"to_do")
    for npc in npc_list:
        id, type, name = npc
        keyboard.button(text=type + " " + name, callback_data=f"npc_{id}")
    for enemy in enemy_list:
        id, type, name, defeated = enemy
        keyboard.button(text=DEFEATED_ENEMY.get(defeated) +
                        " " + type + " " + name, callback_data=f"enemy_{id}")
    keyboard.adjust(1)
    return keyboard


def talk_to_npc_keyboard(npc, npc_id: int) -> InlineKeyboardBuilder:
    """
    Создает клавиатуру для взаимодействия с NPC.
    Параметры:
    - npc: Информация о NPC.
    - npc_id: ID NPC.
    Возвращает:
    - InlineKeyboardBuilder: Построенную клавиатуру.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="❌ У меня приступ социофобии ❌",
                    callback_data="characters")
    keyboard.button(text=READ_NPC.get(npc.dialogue_done) + "Внять мудрость от этого пожилого",
                    callback_data=f"talknpc_{npc_id}_dialogue")
    if npc.knowledge_info:
        keyboard.button(text=READ_NPC.get(npc.knowledge_done) + "Узнать new alco в своей жизни",
                        callback_data=f"talknpc_{npc_id}_knowledge")
    if npc.recipe_info:
        keyboard.button(text=READ_NPC.get(npc.recipe_done) + "Порадовать свои вкусовые сосочки",
                        callback_data=f"talknpc_{npc_id}_recipe")
    if npc.bartender_info:
        keyboard.button(text=READ_NPC.get(npc.bartender_done) + "Взять какую-то барманскую херню",
                        callback_data=f"talknpc_{npc_id}_bartender")
    if npc.quest:
        keyboard.button(text=READ_NPC.get(npc.quest_done) + "Оказать услугу за бабки",
                        callback_data=f"talknpc_{npc_id}_quest")
    return keyboard.adjust(1)


async def choose_npc_to_talk(callback_query: CallbackQuery, data: str, user_id: int) -> None:
    """
    Функция для выбора NPC для разговора.
    Параметры:
    - callback_query: Объект callback_query.
    - data: Данные из коллбэк-данных.
    - user_id: ID пользователя.

    """
    npc_id = int(data.split("_")[1])
    npc = get_npc_info(npc_id)
    if npc:
        response = (f"{npc.type} {npc.name} вещает о том, что ты {random.choice(['чучуло', 'овощной суп', 'лошара', 'курица', 'шалопай', 'пугало'])}\n\n"
                    "Ответь ему, голодранцу.")
        await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
        keyboard = talk_to_npc_keyboard(npc, npc_id)
        await callback_query.answer(response, reply_markup=keyboard.as_markup())
    else:
        await callback_query.answer("НПС сломались и не хотят с вами разговаривать")


async def talk_to_npc(callback_query: CallbackQuery, data: str, user_id: int) -> None:
    """
    Функция для взаимодействия с NPC в зависимости от типа взаимодействия.
    Параметры:
    - callback_query: Объект callback_query.
    - data: Данные из коллбэк-данных.
    - user_id: ID пользователя.
    """
    data_parts = data.split('_')
    npc_id = int(data_parts[1])
    interaction_type = data_parts[2]
    npc = get_npc_info(npc_id)
    if interaction_type == "dialogue":
        update_npc_data("dialogue_done", 1, npc_id)
        await callback_query.answer("🗣 " + npc.dialogue)
    elif interaction_type == "knowledge":
        update_npc_data("knowledge_done", 1, npc_id)
        await knowledge_npc(callback_query, npc)
    elif interaction_type == "recipe":
        update_npc_data("recipe_done", 1, npc_id)
        await recipe_npc(callback_query, npc)
    elif interaction_type == "bartender":
        update_npc_data("bartender_done", 1, npc_id)
        await bartender_npc(callback_query, npc)

    if interaction_type == "quest":
        await quest.quest(callback_query, npc, npc_id, user_id)
    else:
        time.sleep(1)
        await talk_to_npc_next_keyboard(callback_query, user_id, npc_id, npc)


async def talk_to_npc_next_keyboard(callback_query: CallbackQuery, user_id: int, npc_id: int, npc: NPC) -> None:
    """
    Создает клавиатуру для следующего взаимодействия с NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    - npc_id: ID NPC.
    - npc: NPC
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="💬 О да, готов слушать твои уста вечно.",
                    callback_data=f"npc_{npc_id}")
    keyboard.button(
        text="🤦‍♀️ Хочу talk с более адекватными людьми", callback_data="characters")
    keyboard.button(
        text="👯‍♀️ Я устал разговаривать, я хочу тусить", callback_data="to_do")
    keyboard.adjust(1)
    await callback_query.answer(f"🗣 Ты такоооооооой интересный собеседник\n\nЕщё поболтаём c {npc.type} {npc.name}?", reply_markup=keyboard.as_markup())


async def knowledge_npc(callback_query: CallbackQuery, npc) -> None:
    """
    Функция для отображения знаний NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - npc: Информация о NPC.
    """
    await callback_query.answer("🗣 Ща такое расскажу, офигеешь.")
    time.sleep(1)
    response = npc.share_knowledge()
    if '-' in response:
        photo_name = response.split()[0]
        photo = FSInputFile(f'images/alcohol/{photo_name}.jpeg')
        await callback_query.answer_photo(photo, has_spoiler=False)
    await callback_query.answer("🗣 " + response)


async def recipe_npc(callback_query: CallbackQuery, npc) -> None:
    """
    Функция для отображения рецепта от NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - npc: Информация о NPC.
    """
    await callback_query.answer("🗣 Рецепт просто бомба.\nОбязательно попробуй, "
                                "когда заработаешь денег больше, чем на бутылку балтики семерки.")
    time.sleep(1)
    response = npc.share_recipe()
    if '-' in response:
        photo_name = response.split()[1]
        photo = FSInputFile(f'images/recipes/{photo_name}.jpeg')
        await callback_query.answer_photo(photo, has_spoiler=False)
    await callback_query.answer("🗣 " + response)


async def bartender_npc(callback_query: CallbackQuery, npc) -> None:
    """
    Функция для отображения предмета от NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - npc: Информация о NPC.
    """
    await callback_query.answer("🗣 Сейчас я тебе дам барменскую штуку.\n"
                                "Ты спросишь зачем?\n"
                                "А я тебе скажу, что мне эта фигня тоже не нужна.")
    time.sleep(1)
    response = npc.share_item()
    if '-' in response:
        photo_name = response.split()[0]
        photo = FSInputFile(f'images/bartender/{photo_name}.jpeg')
        await callback_query.answer_photo(photo, has_spoiler=False)
    await callback_query.answer("🗣 " + response)
