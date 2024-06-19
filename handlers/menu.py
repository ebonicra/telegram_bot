from aiogram import types
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from . import npc

from . import location, main_buttons
from database.initialization_db import create_enemy, create_new_user, create_npc, create_quest
from database.get_db import get_user_data, get_npc_list, get_enemy_list, reset_user_data
from players_classes import Protagonist


async def send_welcome(message: types.Message) -> None:
    """
    Функция отправляет приветственное сообщение новому пользователю.
    Параметры:
        message (types.Message): Объект сообщения от пользователя.
    """
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user = get_user_data("id", user_id)
    if user is None:
        create_new_user(user_id, user_name)
        create_npc(user_id)
        create_enemy(user_id)
        create_quest(user_id)
        welcome_text = (f"🐌 Привет, {user_name}! Ты - улитка, которая зашла в бар.\n"
                        "Общайся с местным контингентом и попробуй перепить барменов, ведь это твои злейшие враги!\n"
                        "Узнавай новые рецепты коктейлей и алкогольные напитки, "
                        "что поможет тебе быть более эрудированным и меньше пьянеть.\n"
                        "Победи всех и стань самой \"да я не ваще не пьяная, я себя контро... ИК ...лирую\" улиткой!\n\n"
                        "Удачи и вкусной игры!")
        await message.answer(welcome_text)
        await send_rules(message)
    else:
        await message.answer("🐌 Дорогуша, ты забыла? Ты уже тут была.\n"
                             "А ну быстро выпила штрафную и го играть.")
        await main_buttons.send_main_menu(message, user_id)


async def send_info(message: types.Message, user_id: int) -> None:
    """
    Функция отправляет информацию о пользователе.
    Параметры:
        message (types.Message): Объект сообщения от пользователя.
        user_id (int): ID пользователя.
    """
    protagonist = Protagonist(user_id, 'default')
    response = protagonist.whoami()
    if not response:
        await message.answer("Ты ещё не попал в наш шикарный бар. Используйте команду /start чтобы начать игру.")
    else:
        await message.answer(response)
        await main_buttons.deactivate_buttons(message, user_id, message.message_id)
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="⬅ Назад, плиз ⬅", callback_data="send_main_menu")
        await message.answer("Вот как-то так и никак иначе.\n\n"
                             "Иди ещё потыкайся, узнай о себе что-нибудь новое.", reply_markup=keyboard.as_markup())


async def send_inventory(message: types.Message, user_id: int) -> None:
    """
    Функция отправляет инвентарь пользователя.
    Параметры:
        message (types.Message): Объект сообщения от пользователя.
        user_id (int): ID пользователя.
    """
    user = get_user_data("id", user_id)
    if user is None:
        await message.answer("Твои карманы пусты, брат, потому что ты ещё не нажал кнопку /start")
    else:
        await main_buttons.deactivate_buttons(message, user_id, message.message_id)
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="Что там по алкоголю?",
                        callback_data="inventory_knowledge")
        keyboard.button(text="Что там по рецептам?",
                        callback_data="inventory_recipes")
        keyboard.button(text="Что там по барменским штукам?",
                        callback_data="inventory_items")
        keyboard.button(text="Что там по ништякам?",
                        callback_data="inventory_other")
        keyboard.button(text="⬅ Назад, плиз ⬅", callback_data="my_snail")
        keyboard.adjust(1)
        await message.answer("Держи свой багаж, дружочек-пирожечек.\nТыкай на интересующую тебя извилину твоего улиточного мозга.", reply_markup=keyboard.as_markup())


async def send_characters(message: types.Message, user_id: int) -> None:
    """
    Функция отправляет персонажей на текущей локации.
    Параметры:
        message (types.Message): Объект сообщения от пользователя.
        user_id (int): ID пользователя.
    """
    location_id = get_user_data("current_location_id", user_id)
    if location_id:
        npc_list = await get_npc_list(location_id, user_id)
        enemy_list = await get_enemy_list(location_id, user_id)

        if npc_list or enemy_list:
            response = ("Фантастические твари и именно тут они обитают\n\n"
                        "Выбирай любую и тыкай на неё, может что хорошего узнаешь.")
            await main_buttons.deactivate_buttons(message, user_id, message.message_id)
            keyboard = await npc.create_character_keyboard(npc_list, enemy_list)
        else:
            response = "Упссссс. На этой локации никого нет. Не знаю, что произошло, но нажми на /start"
        await message.answer(response, reply_markup=keyboard.as_markup())
    else:
        await message.answer("Никого тут нет. Тебя тоже тут нет. Нажми кнопку /start")


async def send_location(message: types.Message, user_id: int) -> None:
    """
    Функция отправляет информацию о текущей локации и изображение.
    Параметры:
        message (types.Message): Объект сообщения от пользователя.
        user_id (int): ID пользователя.
    """
    user = get_user_data("id", user_id)
    if user is None:
        await message.answer("Локации нет, а значит самое время нажать кнопочку /start.")
    else:
        protagonist = Protagonist(user_id, 'default')
        img_location, response = protagonist.whereami()
        photo = FSInputFile(f'{img_location}')
        await message.answer_photo(photo, has_spoiler=False)
        await message.answer(response)
        await location.move_location(message, user_id, protagonist.current_location_id)


async def send_scheme(message: types.Message, user_id: int) -> None:
    """
    Функция отправляет информацию о схеме бара.
    Параметры:
        message (types.Message): Объект сообщения от пользователя.
        user_id (int): ID пользователя.
    """
    user_location = get_user_data("current_location_id", user_id)
    if user_location is None:
        await message.answer("Схемы нет, а значит самое время нажать кнопочку /start.")
    else:
        photo = FSInputFile(f'images/scheme/scheme_{user_location}.png')
        await message.answer_photo(photo, has_spoiler=False)
        await message.answer("Малышка потерялась? Малышка не теряйся.")
        await location.move_location(message, user_id, user_location)


async def new_game(message: types.Message) -> None:
    """
    Функция отправляет сообщение с предложением начать новую игру.
    Параметры:
        message (types.Message): Объект сообщения от пользователя.
    """
    user_id = message.from_user.id
    await main_buttons.deactivate_buttons(message, user_id, message.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="👶 New game 👶", callback_data="new_game_yes")
    keyboard.button(text="👴 Old game 👴", callback_data="send_main_menu")
    await message.answer("Чувак, это серьёзный шаг, ты уверен?", reply_markup=keyboard.as_markup())


async def new_game_yes(message: types.Message, user_id: int) -> None:
    """
    Функция обрабатывает подтверждение начала новой игры.
    Параметры:
        message (types.Message): Объект сообщения от пользователя.
        user_id (int): ID пользователя.
    """
    reset_user_data(user_id)
    await message.answer("Пришел Танос и стер тебя с половиной Вселенной.\nНажми /start, чтоб воскреснуть.")


async def send_rules(message: types.Message) -> None:
    """
    Функция отправляет правила игры.
    Параметры:
        message (types.Message): Объект сообщения от пользователя.
    """
    user_id = message.from_user.id
    user = get_user_data("id", user_id)
    rules_text = (
        "Правила игры:\n\n"
        "🔸 Ты - улитка!\n"
        "🔸 У тебя есть какой-то уровень айкью. Чем он выше, тем меньше ты пьянеешь.\n"
        "🔸 Повысить свой айкью ты можешь общаясь с разными персонажами, "
        "узнавая у них новые виды алкоголя, рецепты коктейлей или барменские приблуды.\n"
        "🔸 Бармены - твои главные враги, их надо перепить.\n"
        "🔸 У барменов тоже есть свой уровень айкью, и если он выше твоего, то пить с этим барменом пока ты не сможешь.\n"
        "🔸 Чтобы перепить бармена надо выкинуть виртуальный кубик. Чем выше значение на кубике, тем выше урон опьянению.\n"
        "🔸 Некоторые персонажи могут давать тебе квесты. За прохождение квестов ты получаешь money.\n"
        "🔸 Money можно потратить в магазине на всякую дребедень.\n"
        "🔸 Если ты слишком пьян - советую сходить в туалет проветриться.\n"
        "🔸 В игре несколько локаций, на каждой локации свои персонажи и свои приколы.\n"
        "Если всё совсем плохо или ты что-то забыл, там внизу в меню есть разные кнопочки с командами, которые тебе помогут.\n"
        "Вроде всё.\n"
        "Если что-то непонятно - это твои проблемы."
    )
    if user is None:
        await message.answer("Пока не нажмешь кнопку /start все правила бессмыслены.")
        await message.answer(rules_text)
    else:
        await message.answer(rules_text)
        await main_buttons.send_main_menu(message, user_id)
