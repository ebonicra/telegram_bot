from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import time

from database.get_db import get_enemy_info, get_user_data, get_count_defeated_enemy
from . import npc
from . import main_buttons, handlers
from players_classes import Protagonist, Enemy
from bot import bot


def talk_to_enemy_keyboard(enemy_id: int, enemy: Enemy) -> InlineKeyboardBuilder:
    """
    Создает клавиатуру для взаимодействия с врагом.
    Параметры:
    - enemy_id: ID врага.
    - enemy: Информация о враге.
    Возвращает:
    - InlineKeyboardBuilder: Клавиатура для взаимодействия с врагом.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="❌ У меня приступ социофобии ❌",
                    callback_data="characters")
    keyboard.button(text="Слыш, улитка, поговорим?",
                    callback_data=f"talkenemy_{enemy_id}_dialogue")
    keyboard.button(text="Го кто кого перепьёт?",
                    callback_data=f"talkenemy_{enemy_id}_drink")
    keyboard.button(text=f"Кто {enemy.name} по жизни?",
                    callback_data=f"talkenemy_{enemy_id}_info")
    return keyboard.adjust(1)


async def choose_enemy_to_talk(callback_query: CallbackQuery, data: str, user_id: int) -> None:
    """
    Обработчик выбора врага для разговора.
    Параметры:
    - callback_query: Объект callback_query.
    - data: Данные из callback_data.
    - user_id: ID пользователя.
    """
    enemy_id = int(data.split("_")[1])
    enemy = get_enemy_info(enemy_id)
    if enemy:
        response = (f"{npc.DEFEATED_ENEMY.get(enemy.defeated)} {enemy.type} {enemy.name} быкует на тебя.\n\n"
                    "Разберись по-мужски с ним.\n"
                    "Ты вообще улитка или сопля какая-то?")
        await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
        keyboard = talk_to_enemy_keyboard(enemy_id, enemy)
        await callback_query.answer(response, reply_markup=keyboard.as_markup())
    else:
        await callback_query.answer("Бармены сломались и не хотят с вами разговаривать")


async def talk_to_enemy(callback_query: CallbackQuery, data: str, user_id: int) -> None:
    """
    Обработчик разговора с врагом.
    Параметры:
    - callback_query: Объект callback_query.
    - data: Данные из callback_data.
    - user_id: ID пользователя.
    """
    data_parts = data.split('_')
    enemy_id = int(data_parts[1])
    interaction_type = data_parts[2]
    enemy = get_enemy_info(enemy_id)
    if interaction_type == "dialogue":
        await callback_query.answer("🗣 " + enemy.dialogue)
    elif interaction_type == "info":
        response = enemy.whoisenemy()
        await callback_query.answer("🗣 " + response)
    if interaction_type == "drink":
        await what_drink(callback_query, enemy_id, enemy, user_id)
    else:
        await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="⬅ Назад, плиз ⬅",
                        callback_data=f"enemy_{enemy_id}")
        time.sleep(1)
        await callback_query.answer("🗣 Чтоооо? Нечего мне возразить? "
                                    "Пришла тут улитка сопливая, от работы только отвлекает.\nВали пока не поздно.", reply_markup=keyboard.as_markup())


async def what_drink(callback_query: CallbackQuery, enemy_id: int, enemy: Enemy, user_id: int) -> None:
    """
    Обработчик выбора напитка для битвы.
    Параметры:
    - callback_query: Объект callback_query.
    - enemy_id: ID врага.
    - enemy: Информация о враге.
    - user_id: ID пользователя.
    """
    knowledge = get_user_data("knowledge", user_id)
    intoxication_level = get_user_data("intoxication_level", user_id)
    alcohol_knowledge = get_user_data("alcohol_knowledge", user_id)
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()

    if intoxication_level >= 10000:
        response = ("🗣 Куда тебе пить то, ты дурёха. Низя-низя, иди трезвей.")
    elif len(alcohol_knowledge) == 0:
        response = ("🗣 Ты ещё слишком маленький и несмышленный, чтобы пить.\n"
                    "Иди лучше молочка попей, может это поможет твоему умственному развитию.")
    elif knowledge < enemy.knowledge:
        response = ("🗣 Я тебя не уважаю, чтоб с тобой пить.\n"
                    "У тебя даже уровень айкью ниже, чем у меня, не говоря о том, что ты вообще улитка.")
    else:
        response = "🗣 Что пить будем?\n\nУчти, тут всё пьют только шотами.\nЕсли ссышь, лучше сразу сдайся."
        for alco in alcohol_knowledge.keys():
            keyboard.button(
                text=f"💥 {alco} 💥", callback_data=f"drinkenemy_{alco}_{enemy_id}")

    keyboard.button(text="⬅ Назад, плиз ⬅", callback_data=f"enemy_{enemy_id}")
    keyboard.adjust(2) if len(alcohol_knowledge) > 5 else keyboard.adjust(1)
    await callback_query.answer(response, reply_markup=keyboard.as_markup())


async def drink_enemy(callback_query: CallbackQuery, data: str, user_id: int) -> None:
    """
    Обработчик выбора напитка для врага.
    Параметры:
    - callback_query: Объект callback_query.
    - data: Данные из callback_data.
    - user_id: ID пользователя.
    """
    data_parts = data.split('_')
    alco = data_parts[1]
    enemy_id = int(data_parts[2])
    enemy = get_enemy_info(enemy_id)
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    count = get_count_defeated_enemy(user_id)
    if count >= 5 or enemy.defeated:
        await handle_defeated_enemy(callback_query, enemy, alco, enemy_id, keyboard)
    else:
        await handle_enemy_drinking(callback_query, enemy, alco, enemy_id, user_id, count, keyboard)


async def handle_defeated_enemy(callback_query: CallbackQuery, enemy: Enemy, alco: str, enemy_id: int, keyboard: InlineKeyboardBuilder) -> None:
    """
    Обработчик для случая, когда враг уже был побежден.
    Параметры:
    - callback_query: Объект callback_query.
    - enemy: Информация о враге.
    - alco: Напиток, выбранный пользователем.
    - enemy_id: ID врага.
    - keyboard: Клавиатура для сообщения.
    """
    keyboard.button(text="⬅ Назад, плиз ⬅", callback_data=f"characters")
    if enemy.defeated:
        await callback_query.answer(f"🗣 Не, родненькая, твоя взяла, я слабак и чепушила.\n\n"
                                    f"Я больше не буду пить, даже если это {alco.lower()}", reply_markup=keyboard.as_markup())
    else:
        await callback_query.answer(f"🗣 Никто с тобой больше пить не будет. "
                                    f"Ни {alco.lower()}, ни что-либо другое. Уходи отсюда.", reply_markup=keyboard.as_markup())


async def handle_enemy_drinking(callback_query: CallbackQuery, enemy: Enemy, alco: str, enemy_id: int, user_id: int, count: int, keyboard: InlineKeyboardBuilder) -> None:
    """
    Обработчик для выпивки с врагом.
    Параметры:
    - callback_query: Объект callback_query.
    - enemy: Информация о враге.
    - alco: Напиток, выбранный пользователем.
    - enemy_id: ID врага.
    - user_id: ID пользователя.
    - count: Количество побежденных врагов пользователем.
    - keyboard: Клавиатура для сообщения.
    """
    alcohol_knowledge = get_user_data("alcohol_knowledge", user_id)
    await callback_query.answer(f"🗣 Ого, {alco.lower()} - хороший выбор.\n"
                                "Хотя когда ты улитка в баре для тебя всё хороший выбор.\n"
                                "Просто напомню, родная, чем ты собираешься себя травить:\n\n"
                                f"{alco} - {str(alcohol_knowledge.get(alco))}")

    await callback_query.answer(f"Бармен {enemy.name} бросает кубик:")
    enemy_dice_message = await bot.send_dice(user_id, emoji="🎲")
    enemy_dice_value = enemy_dice_message.dice.value
    response, finish = enemy.drink(enemy_dice_value, count)
    time.sleep(5)
    for i in response:
        await callback_query.answer(i)
        time.sleep(1)
    if finish:
        keyboard.button(text="👑 Быть победителем! 👑",
                        url="https://www.youtube.com/watch?v=ziR_C0TXW2Q")
        await callback_query.answer(f"Мама-мия, да ты всех перерпил.\n"
                                    "Да ты невероятен.\nТы неповторим.\nТы - легенда!", reply_markup=keyboard.as_markup())
        time.sleep(5)
        await winner(callback_query, user_id)
    else:
        handlers.user_states[user_id] = "awaiting_dice"
        keyboard.button(text="🎲 Бросить кубик 🎲",
                        callback_data=f"drinksnail_{enemy_id}")
        await callback_query.answer(f"Твоя очередь бросать кубик.\nНе ссы, {alco.lower()} - это вкусно.", reply_markup=keyboard.as_markup())


async def drink_snail(callback_query: CallbackQuery, data: str, user_id: int) -> None:
    """
    Обработчик броска кубика пользователем.
    Параметры:
    - callback_query: Объект callback_query.
    - data: Данные из callback_data.
    - user_id: ID пользователя.
    """
    handlers.user_states[user_id] = "OK"
    enemy_id = int(data.split("_")[1])
    await callback_query.answer("Ты бросаешь кубик:")
    user_dice_message = await bot.send_dice(user_id, emoji="🎲")
    user_dice_value = user_dice_message.dice.value
    protagonist = Protagonist(user_id, 'default')
    response = protagonist.drink(user_dice_value)
    time.sleep(5)
    for i in response:
        await callback_query.answer(i)
        time.sleep(1)

    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⬅ Назад, плиз ⬅", callback_data=f"enemy_{enemy_id}")
    await callback_query.answer(f"Хорош пить, иди проветрись.", reply_markup=keyboard.as_markup())


async def winner(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик завершения игры с победой.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    keyboard = InlineKeyboardBuilder()
    await callback_query.answer("🔥 Поздравляю, мой юный алкоголик, ты - победил! 🔥")
    keyboard.button(text="Начать новую игру", callback_data=f"new_game")
    keyboard.button(text="Продолжить слонятся тут без дела",
                    callback_data=f"to_do")
    keyboard.button(text="Бросить пить", callback_data=f"anti_winner")
    keyboard.adjust(1)
    await callback_query.answer(f"Что будем делать дальше?", reply_markup=keyboard.as_markup())


async def anti_winner(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик для случая, когда пользователь отказывается от победы.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    await callback_query.answer("🤣 Не поможет ахахахахахаах 🤣")
    keyboard.button(text="⬅ Назад, плиз ⬅", callback_data=f"winner")
    await callback_query.answer(f"Что будем делать дальше?", reply_markup=keyboard.as_markup())
