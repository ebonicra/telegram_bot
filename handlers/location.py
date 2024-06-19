from aiogram import types
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
import time
import random

from players_classes import Protagonist
from database.get_db import get_path_data, get_location_data, get_quest_data, get_user_data, update_quest_data, update_user_data
from . import main_buttons, menu


DIRECTION_ARROWS = {
    "up": "⬆️",
    "left": "⬅️",
    "right": "➡️",
    "down": "⬇️"
}

CIGARETTE = [
    "🎵  2000 баксов",
    "🎵  За сигарету",
    "🎵  И даже полжизни",
    "🎵  Не жалко за это",
    "🎵  Чуть-чуть покурить",
    "🎵  И до рассвета",
    "🎵  Будем летать",
    "🎵  Чтобы снова отдать",
    "🎵  2000 баксов!"
]

ROOF = [
    "🎵  Скоро рассвет,",
    "🎵  Выхода нет",
    "🎵  Ключ поверни",
    "🎵  И полетели",
    "🎵  Нужно писать",
    "🎵  В чью-то тетрадь",
    "🎵  Кровью, как в метрополитене",
    "🎵  Выхода нет",
    "🎵  Выхода нет!"
]


async def move_location(message: types.Message, user_id: int, location_id: int = None) -> None:
    """
    Функция для перемещения пользователя в новую локацию.
    Параметры:
    - message: Объект сообщения типа Message.
    - user_id: ID пользователя.
    - location_id: ID текущей локации пользователя.
    """
    if not location_id:
        location_id = get_user_data("current_location_id", user_id)
    location_name = get_location_data("name", location_id)
    await main_buttons.deactivate_buttons(message, user_id, message.message_id)
    keyboard = InlineKeyboardBuilder()
    directions = get_path_data(location_id)
    for new_location_id, direction in directions:
        arrow = DIRECTION_ARROWS.get(direction, "")
        new_location_name = get_location_data("name", new_location_id)
        button_text = f"{arrow} {new_location_name}"
        callback_data = f"go_{new_location_id}"
        keyboard.button(text=button_text, callback_data=callback_data)
    keyboard.button(text="🚷 Никуда не пойду. Тут упаду.",
                    callback_data="to_do")
    keyboard.adjust(2)
    response = f"📌 Щас мы тут: {location_name.lower()}\n\nНо вопрос в другом, где мы окажемся через секунду?"
    await message.answer(response, reply_markup=keyboard.as_markup())


async def go_to_new_location(callback_query: CallbackQuery, user_id: int, data: str) -> None:
    """
    Функция для перехода в новую локацию по нажатию кнопки.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    - data: Данные из callback_data (ID новой локации).
    """
    new_location_id = int(data.split("_")[1])
    protagonist = Protagonist(user_id, 'default')
    protagonist.go(new_location_id)
    img_location, response = protagonist.whereami()
    photo = FSInputFile(f'{img_location}')
    await callback_query.answer_photo(photo, has_spoiler=False)
    await callback_query.answer(response)
    await main_buttons.to_do(callback_query, user_id)


async def find_fun(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Функция для поиска развлечений на текущей локации.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    data = get_user_data("current_location_id", user_id)
    if data:
        if data == 4:
            await toilet(callback_query, user_id)
        elif data == 7:
            await hall(callback_query, user_id)
        elif data == 8:
            await market(callback_query, user_id)
        elif data == 6:
            await roof(callback_query, user_id)
        else:
            await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
            keyboard = InlineKeyboardBuilder()
            keyboard.button(text="⬅ Назад, плиз ⬅", callback_data=f"to_do")
            response = ("Ничего тут нет интересного.\n\n"
                        "Только огромная душевная пустота и космическое одиночество.")
            await callback_query.answer(response, reply_markup=keyboard.as_markup())


async def toilet(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Функция для обработки действий в туалете.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await callback_query.answer("Ты чегоооо?\n"
                                "Не признал что-ли своего друга?\n"
                                "Своего товарища и единомышленника?")
    time.sleep(1)
    await callback_query.answer("🚽 Это же его величество унитаз! 🚽")
    time.sleep(1)
    await callback_query.answer("Если использовать белый трон по назначению, то можно немного облегчить свою ношу алкогольного опьянения.\n\n"
                                "Правила просты:\n"
                                "1) Прицеливаешься нужным отверстием в дырочку унитаза. "
                                "Главное не промахнись.\n"
                                "2) Испускаешь из себя некоторую субстанцию.\n"
                                "3) В конце нажимаешь на кнопочку и грязь уходит.\n")
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="☺️ Use toilet ☺️", callback_data=f"toilet")
    keyboard.button(text="⬅ Назад, плиз ⬅", callback_data=f"to_do")
    time.sleep(1)
    await callback_query.answer("Ссым или не ссым?", reply_markup=keyboard.as_markup())


async def use_toilet(callback_query: CallbackQuery, user_id: int, user_name: str) -> None:
    """
    Функция для использования унитаза.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    - user_name: Имя пользователя.
    """
    await callback_query.answer("🤮 Кхреее кхрее кхреееее 🤮")
    time.sleep(0.5)
    await callback_query.answer("💦 Пись пииись пииииииись 💦")
    time.sleep(0.5)
    await callback_query.answer("💩 Бульк бульк буууульк 💩")
    time.sleep(0.5)
    await callback_query.answer("*Звуки смыва унитаза*")
    time.sleep(0.5)
    await callback_query.answer(f"👍 Well done, {user_name}, well done! 👍")
    time.sleep(0.5)
    intoxication = get_user_data("intoxication_level", user_id)
    if intoxication >= 1000:
        intoxication -= 1000
        update_user_data("intoxication_level", intoxication, user_id)
        await callback_query.answer(f"Благодаря данной манипуляции тебе удолось немного протрезветь.\nТеперь твой уровень опьянения состовляет {intoxication // 1000} из 10.")
    else:
        await callback_query.answer(f"Трезветь тебе больше некуда, но зато получил удовольствие, правда же?")
    time.sleep(0.5)
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="☺️ Ещё use ☺️", callback_data=f"toilet")
    keyboard.button(text="⬅ Назад, плиз ⬅", callback_data=f"to_do")
    await callback_query.answer("Ну вот, умничка.\nЗапомни - эта белая штука - твоя подруга.\nПриходи сюда, когда будет плохо.", reply_markup=keyboard.as_markup())


async def hall(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Функция для обработки действий в коридоре.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await callback_query.answer("Классный тут вайб всё-таки.\nЭто лучший бар, чтоб напиться в сопельки!")
    time.sleep(1)
    await callback_query.answer("Тааак, а это что у нас такое?\n\nМдааааа\n\nНеоновая вывеска, чтоб всякие пьяные тупые малолетки делали ещё более тупые селфи?")
    time.sleep(1)
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🤳 Сделать селфи 🤳", callback_data=f"selfie")
    keyboard.button(text="⬅ Назад, плиз ⬅", callback_data=f"to_do")
    await callback_query.answer("Я, конечно, не малолетка, но всё такая же пьяная и тупая.\nПу-пу-пуууууу", reply_markup=keyboard.as_markup())


async def use_hall(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Функция для использования функций коридора.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await callback_query.answer("Я такаааааая красиваяяяяяяяяяя")
    i = random.randint(1, 8)
    photo = FSInputFile(f'images/selfie/snail_{i}.jpeg')
    await callback_query.answer_photo(photo, has_spoiler=True)
    count_selfie = get_quest_data("count", "Selfie", user_id)
    update_quest_data("count", count_selfie + 1, "Selfie", user_id)
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🤳 Сделать ещё селфи 🤳", callback_data=f"selfie")
    keyboard.button(text="⬅ Назад, плиз ⬅", callback_data=f"to_do")
    await callback_query.answer("Главное не смотреть на это фото, когда буду трезвой.", reply_markup=keyboard.as_markup())


async def roof(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Функция для обработки действий на крыше.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await callback_query.answer("Ммммм, какой вид, какая красота.")
    time.sleep(1)
    await callback_query.answer("Ебааааа, а как высоко то...")
    time.sleep(1)
    await callback_query.answer("... а вот бы спрыгнуть с крыши ахахаха ...")
    time.sleep(1)
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🧚 Прыг с крыши 🧚", callback_data=f"roof")
    keyboard.button(text="⬅ Назад, плиз ⬅", callback_data=f"to_do")
    await callback_query.answer("Сейчас или никогда.\nСейчас или никогда.\nСейчас или никогда.\n", reply_markup=keyboard.as_markup())


async def use_roof(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Функция для использования действий на крыше.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    count_fall = get_quest_data("count", "Roof", user_id) + 1
    update_quest_data("count", count_fall, "Roof", user_id)
    if count_fall <= 2:
        await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="⬅ Назад, плиз ⬅", callback_data=f"to_do")
        await callback_query.answer("Ты чё, дурочок совсем?\nИди отсюда, пока жив.\n", reply_markup=keyboard.as_markup())
    else:
        for i in ROOF:
            await callback_query.answer(i)
            time.sleep(1)
        await callback_query.answer("👼🏻 Поздравляю, ты упал и разбился в шмакодявку 👼🏻\n\nИди, начинай игру заново.")
        time.sleep(1)
        await menu.new_game_yes(callback_query, user_id)


async def market(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Функция для обработки действий в магазине.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await callback_query.answer("Ой, а откуда такие хилинькие огонечки светится?\nДа это же ночной ларёк.")
    time.sleep(1)
    await callback_query.answer("Ой, а кто это там сегодня продавщица?\n\nДа это же моя любимая тетя Вася.")
    time.sleep(1)
    await callback_query.answer("😍😍😍😍😍😍😍😍😍😍😍😍😍😍😍😍😍😍😍😍😍😍😍😍\n\nСамая красивая и самая сексуальная тетя Вася.")
    time.sleep(1)
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🛒 Зайти в магазин 🛒", callback_data=f"market")
    keyboard.button(text="⬅ Назад, плиз ⬅", callback_data=f"to_do")
    await callback_query.answer("Нам определенно туда надо зайти. "
                                "Самое свежее мясо и самая вкусная палёнка только там и нигде больше.", reply_markup=keyboard.as_markup())


async def use_market(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Функция для использования функций магазина.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    response = ("Года идут, а ассартимент не устаёт удивлять.\nВроде у меня есть немного тенге, надо купить какую-нибудь бесполезную херь.")
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="🌹 Цветы для любимой улиточки 🌹",
                    callback_data=f"buy_flower")
    keyboard.button(text="🔞 Презервативы \"Гороскоп\" 🔞",
                    callback_data=f"buy_condom")
    keyboard.button(text="🥐 Круассан 🥐", callback_data=f"buy_croissant")
    keyboard.button(text="🐟 Горбуша 🐟", callback_data=f"buy_fish")
    keyboard.button(text="💊 Аспирин 💊", callback_data=f"buy_pill")
    keyboard.button(text="🌻 Семечка 🌻", callback_data=f"buy_seed")
    keyboard.button(text="🚬 Сигареты 🚬", callback_data=f"buy_cigarette")

    keyboard.button(text="⬅ Назад, плиз ⬅", callback_data=f"to_do")
    keyboard.adjust(1)
    await callback_query.answer(response, reply_markup=keyboard.as_markup())


async def buy_market(callback_query: CallbackQuery, data: str, user_id: int) -> None:
    """
    Функция для обработки покупок в магазине.
    Параметры:
    - callback_query: Объект callback_query.
    - data: Данные из коллбэк-данных.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()

    product = data.split('_')[1]
    if product == 'flower':
        await callback_query.answer("🌹 Значит цветочки?")
        await callback_query.answer("На любимых экономить нельзя. Так что эти волшебные flowers стоят 800 деняк.")
        keyboard.button(text="Да", callback_data=f"pay_800_Цветочки")
    elif product == 'condom':
        await callback_query.answer("🔞 Значит презервативы?")
        await callback_query.answer("Лучше сегодня заплатить 500, чем потом выплачивать по 100500 улиточным отпрыскам.")
        keyboard.button(text="Да", callback_data=f"pay_500_Презервативы")
    elif product == 'croissant':
        await callback_query.answer("🥐 Значит круассан?")
        await callback_query.answer("Сладеньких булочек все любят, поэтому всего 150 денег и диабет твой.")
        keyboard.button(text="Да", callback_data=f"pay_150_Круассаны")
    elif product == 'fish':
        await callback_query.answer("🐟 Значит горбуша?")
        await callback_query.answer("Зачем тебе горбуша? Зачем тебе блин горбуша? Ладно, если очень хочешь, то 1000 деняк и вкус рыбы тебе обеспечен.")
        keyboard.button(text="Да", callback_data=f"pay_1000_Горбуша")
    elif product == 'pill':
        await callback_query.answer("💊 Значит аспирин?")
        await callback_query.answer("Что, немолодой уже, раз аспиринчик на утро берешь? Бери, бери, мой милый, 200 деняк и ты будешь жить ещё денёк.")
        keyboard.button(text="Да", callback_data=f"pay_200_Аспирин")
    elif product == 'seed':
        await callback_query.answer("🌻 Значит семечка?")
        await callback_query.answer("Ты дурочок? Зачем тебе одна семечка? Обсосать её и голубям скормить? Ладно, 1 монетка - 1 семечка.")
        keyboard.button(text="Да", callback_data=f"pay_1_Семечка")
    elif product == 'cigarette':
        for i in CIGARETTE:
            await callback_query.answer(i)
            time.sleep(1)
        keyboard.button(text="ДА", callback_data=f"pay_2000_Сигареты")

    keyboard.button(text="НЕТ", callback_data=f"market")
    keyboard.adjust(1)
    await callback_query.answer("Брать будем?", reply_markup=keyboard.as_markup())


async def pay(callback_query: CallbackQuery, data: str, user_id: int) -> None:
    """
    Функция для выполнения оплаты товара в магазине.
    Параметры:
    - callback_query: Объект callback_query.
    - data: Данные из коллбэк-данных.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()

    data_parts = data.split('_')
    cost = int(data_parts[1])
    product = data_parts[2]
    money = get_user_data("money", user_id)
    other_items = get_user_data("other_items", user_id)
    if money >= cost:
        await callback_query.answer(f"Поздравляю с бесполезной покупкой за {cost} money.")
        await callback_query.answer(f"Приходите к нам ещё, мы будем вас ждать.\n\n*Тётя Вася ехидно улыбается*")
        count = other_items.get(product, 0)
        other_items[product] = count + \
            20 if product == 'Сигареты' else count + 1
        update_user_data("money", money-cost, user_id)
        update_user_data("other_items", other_items, user_id)
        keyboard.button(text="Купить ещё что-нибудь", callback_data=f"market")
    else:
        await callback_query.answer(f"Зайка моя, да ты же нищенка.\nНа твоём счёту всего {money} money.")
        await callback_query.answer("Но ты всегда можешь подзаработать у местных ребят.\nКак говорится, с тебя услуга, с них достойная оплата.")
    keyboard.button(text="Уйти нафиг отсюда", callback_data=f"to_do")
    await callback_query.answer("Что дальше будем делать?", reply_markup=keyboard.as_markup())
