from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import time

from players_classes import Protagonist
from database.get_db import get_quest_data, update_quest_data, get_user_data, update_user_data, get_npc_data, update_npc_data
from . import main_buttons


async def quest(callback_query: CallbackQuery, npc, npc_id: int, user_id: int) -> None:
    """
    Обрабатывает квест NPC в зависимости от его названия. Если квест уже выполнен, сообщает об этом.
    Параметры:
    - callback_query: Объект callback_query.
    - npc: Информация о NPC.
    - npc_id: ID NPC.
    - user_id: ID пользователя.
    """
    quest_name = npc.quest
    done_quest = get_quest_data("done", quest_name, user_id)
    if done_quest:
        await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
        keyboard = InlineKeyboardBuilder()
        await callback_query.answer("🗣 Вай-май, моя ты хорошая, ты же уже прошла моё задание.\n"
                                    "Ты уже умничка.\nИ ты уже офигела.\nИди отсюда, мошенница.")
        time.sleep(1)
        keyboard.button(text="⬅ Не быковать и поговорить о другом ⬅",
                        callback_data=f"npc_{npc_id}")
        await callback_query.answer("Туц-туц, улиточка - ты как всегда офигенна.", reply_markup=keyboard.as_markup())
    else:
        if quest_name == 'Bar':
            await quest_bar(callback_query, npc_id, user_id)
        elif quest_name == 'Photographer':
            await quest_photographer(callback_query, npc_id, user_id)
        elif quest_name == 'Recipe':
            await quest_recipe(callback_query, npc_id, user_id)
        elif quest_name == 'Cigarette':
            await quest_cigarette(callback_query, npc_id, user_id)
        elif quest_name == 'Quiz':
            await quest_quiz(callback_query, npc_id, user_id)


async def quest_bar(callback_query: CallbackQuery, npc_id: int, user_id: int) -> None:
    """
    Обрабатывает квест "Bar" NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - npc_id: ID NPC.
    - user_id: ID пользователя.
    """
    await callback_query.answer("🗣 Корочееее, я всегда хотел стать барменом.")
    time.sleep(1)
    await callback_query.answer("🗣 И не просто барменом, а таким секси-шмекси-круто-вау-обалдеть.")
    time.sleep(1)
    await callback_query.answer("🗣 Хочу крутить вот этими прикольными штуками, которые крутят бармены, типа вау фокус-покус и нектар богов.")
    time.sleep(1)
    await callback_query.answer("🗣 Но вот проблема, я понятия не имею, что это за штуки, как они называются и почему я вообще разговариваю с улиткой?")
    time.sleep(1)
    await callback_query.answer("🗣 Помоги мне, помогииии мнееее стать легендой этого бара.")
    time.sleep(1)
    await callback_query.answer("🗣 Расскажи мне хотя бы про 5 барменских штук, а я никому не расскажу, что ты улитка.\nА, ну да, ещё деняк дам.")
    time.sleep(1)
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🧠 Поделиться своими познаниями 🧠",
                    callback_data="bar")
    keyboard.button(text="🙅‍♀️ Нафиг этого бармена недоделанного 🙅‍♀️",
                    callback_data=f"npc_{npc_id}")
    keyboard.adjust(1)
    await callback_query.answer("Что делать будем?", reply_markup=keyboard.as_markup())


async def bar(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обрабатывает результаты квеста "Bar".
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    protagonist = Protagonist(user_id, 'default')
    protagonist.send_inventory()
    count_bartender_items = len(protagonist.bartender_items)
    if count_bartender_items == 0:
        await callback_query.answer("🗣 Ты валенок, ты чё людей то дуришь,\nТы вообще ничего не знаешь о барменских штуках.")
        keyboard.button(
            text="🙁 Идти гулять и барменизироваться 🙁", callback_data="to_do")
    else:
        response = protagonist.send_inventory_type('items')
        for i in response:
            await callback_query.answer(i)
            time.sleep(1)
        await callback_query.answer("Вот это ты выдал базу, вот это ты молодец.\nПосмотрим, что на это скажет чудо(нет)бармен.")
        time.sleep(2)

    if count_bartender_items >= 5:
        await callback_query.answer("🗣 Спасибо дорогуша, ты лучшая из всех этих недружелюбных голодранцев.\n"
                                    "Теперь я буду лучшим барменом этого мироздания.\n"
                                    "Теперь я склоню к алкоголизму весь миииииир.\n\n"
                                    "Ахахахахахахахахахахахахахах")
        time.sleep(1)
        await callback_query.answer("🗣 Ах, да, обещенные денюжки.\nВот, держи, 50 рублей.\n\nЛадно, шучу, держи пятихатку.")
        keyboard.button(text="💵 Взять money и гордиться собой 💵",
                        callback_data="money_500_Bar")
    elif count_bartender_items > 0:
        await callback_query.answer(f"🗣 Неплохо, коненчо, но слабовато.\nTы знаешь всего {count_bartender_items}, а я просил хотя бы 5 барменских штук.")
        keyboard.button(
            text="🙁 Идти гулять и барменизироваться 🙁", callback_data="to_do")
    await callback_query.answer("Выбора нет, надо тыкать на кнопочку ниже:", reply_markup=keyboard.as_markup())


async def quest_photographer(callback_query: CallbackQuery, npc_id: int, user_id: int) -> None:
    """
    Обрабатывает квест "Photographer" NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - npc_id: ID NPC.
    - user_id: ID пользователя.
    """
    await callback_query.answer("🗣 Мию - мяу, ты вообще знал, что я известный фотографеееер?")
    time.sleep(1)
    await callback_query.answer("🗣 Зашел в эту забегаловку, опрокинуть бокальчик мартини и собрать пару фото.")
    time.sleep(1)
    await callback_query.answer("🗣 Я так то сейчас работаю над собственной выставкой \"Убожество и халупа\"")
    time.sleep(1)
    await callback_query.answer("🗣 Ну вообще, ты идеально подходишь для моей коллекции, так что если предоставишь пару своих фото, буду признателен.")
    time.sleep(1)
    await callback_query.answer("🗣 Многого я от тебя не жду, так что можно даже просто селфи сделать. Штук 5-10 сойдет.")
    time.sleep(1)
    await callback_query.answer("🗣 Естественно не бесплатно.\nЗа каждое фото плачу сотку баксов,\nили тенге,\nили юаней,\nкороче, какое настроение будет, то и дам.")
    time.sleep(1)
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📸 Показать свои секси фоточки 📸",
                    callback_data="photographer")
    keyboard.button(text="🙅‍♀️ Нафиг этого фоточкина недоделанного 🙅‍♀️",
                    callback_data=f"npc_{npc_id}")
    keyboard.adjust(1)
    await callback_query.answer("Что делать будем?", reply_markup=keyboard.as_markup())


async def photographer(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обрабатывает результаты квеста "Photographer".
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    count_photo = get_quest_data("count", "Selfie", user_id)
    await callback_query.answer("*Показываешь свои фотОчки*")
    time.sleep(1)
    if count_photo == 0:
        await callback_query.answer("🗣 Ты хотя бы одну фотку сделай, а потом уже приходи ко мне.")
        time.sleep(1)
        await callback_query.answer("🗣 По секрету, в этом баре есть ничё такое место где-то в коридоре, где можно пофотаться.\n"
                                    "Обычно там зумеры ошиваются, но ты представь, что ты тоже молод, и селфись себе на здоровье.")
        keyboard.button(text="🙁 Идти гулять и пофоткаться 🙁",
                        callback_data="to_do")
    elif count_photo >= 5:
        await callback_query.answer("🗣 Дааа, это то самое убожество, что мне и было нужно.")
        time.sleep(1)
        await callback_query.answer(f"🗣 Тааак, ты сфотался {count_photo} раз, значит я тебе должен {count_photo * 100} долларов.")
        keyboard.button(text="💵 Взять money и гордиться собой 💵",
                        callback_data=f"money_{count_photo * 100}_Photographer")
    else:
        await callback_query.answer(f"🗣 Круто-классно конечно, но я просил как минимум 5 фото, а ты сфоткался лишь {count_photo}")
        keyboard.button(text="🙁 Идти гулять и пофоткаться 🙁",
                        callback_data="to_do")
    time.sleep(1)
    await callback_query.answer("Выбора нет, надо тыкать на кнопочку ниже:", reply_markup=keyboard.as_markup())


async def quest_recipe(callback_query: CallbackQuery, npc_id: int, user_id: int) -> None:
    """
    Обрабатывает квест "Recipe" NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - npc_id: ID NPC.
    - user_id: ID пользователя.
    """
    await callback_query.answer("🗣 Факт обо мне: я обожаю Негрони.")
    time.sleep(1)
    await callback_query.answer("🗣 Я просто готов сосать данный божественный коктейль часами и годами.")
    time.sleep(1)
    await callback_query.answer("🗣 Сосать его, глотать его, хлебать его, похлёбывать, а в конце ещё причмокивать.")
    time.sleep(1)
    await callback_query.answer("🗣 Но в этом чмошном баре негрони супер дорогой\nА я сижу у мамке на шее, поэтому не могу себе его позволить.")
    time.sleep(1)
    await callback_query.answer("🗣 Не мог бы ты рассказать мне рецепт данного нектара, а я уже буду его сам готовить и развивать бытовой алкоголизм?")
    time.sleep(1)
    await callback_query.answer("🗣 Да не парься, я заплачу тебе.\nНемного, конечно, что смогу, но заплачу.")
    time.sleep(1)
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🥃 Рассказать рецепт Негрони 🥃",
                    callback_data="recipe")
    keyboard.button(text="🙅‍♀️ Нафиг этого негрониста недоделанного 🙅‍♀️",
                    callback_data=f"npc_{npc_id}")
    keyboard.adjust(1)
    await callback_query.answer("Что делать будем?", reply_markup=keyboard.as_markup())


async def recipe(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обрабатывает результаты квеста "Recipe".
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    protagonist = Protagonist(user_id, 'default')
    protagonist.send_inventory()
    count_cocktail_recipes = len(protagonist.cocktail_recipes)
    negroni = False
    if count_cocktail_recipes == 0:
        await callback_query.answer("🗣 Малышка-глупышка, если не сказать хуже.\nДа ты ж вообще ни одного рецепта не знаешь, фигли тут выпендриваешься?")
    else:
        response = protagonist.send_inventory_type('recipes')
        for i in response:
            if 'Негрони' in i:
                negroni = True
            await callback_query.answer(i)
            time.sleep(1)
        await callback_query.answer("Нифига себе, сколько рецептов ты знаешь, интересно, заплатят ли за это?")
        time.sleep(2)

    if negroni:
        await callback_query.answer("🗣 Вау, вау, вау, спасибо большое, улиточка - улыбочка.\nНаконец-то мой любимый негр... ой ... они.")
        time.sleep(1)
        await callback_query.answer("🗣 Это, конечно, не смысл жизни, но тоже поможет мне прожить ещё несколько дней.\n\nДержи 200 деняк, больше не дам, больше нету.")
        keyboard.button(text="💵 Взять money и гордиться собой 💵",
                        callback_data="money_200_Recipe")
    else:
        await callback_query.answer(f"🗣 Ты дурочка совсем? Тут нет Негрони.")
        time.sleep(1)
        await callback_query.answer(f"🗣 Приходи ко мне, когда узнаешь рецепт того, что я у тебя попросил.")
        keyboard.button(text="🙁 Идти гулять и искать рецепты 🙁",
                        callback_data="to_do")
    time.sleep(1)
    await callback_query.answer("Выбора нет, надо тыкать на кнопочку ниже:", reply_markup=keyboard.as_markup())


async def quest_cigarette(callback_query: CallbackQuery, npc_id: int, user_id: int) -> None:
    """
    Обработчик квеста на сигареты от NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - npc_id: ID NPC.
    - user_id: ID пользователя.
    """
    await callback_query.answer("🗣 Ляяяя, братик, радной\nОй, сестричка то есть.")
    time.sleep(1)
    await callback_query.answer("🗣 Угости сигареткой, плиз плиз.")
    time.sleep(1)
    await callback_query.answer("🗣 Я вaaaбще против курения.\nВaaaaaбще это та ещё гадость.\nПотом ещё воняешь.\nПотом ещё харкаешь.\n")
    time.sleep(1)
    await callback_query.answer("🗣 Да и сагареты я не курю, я парю.\nНу вот знаешь, взять бы дудку со вкусом мохито или чая с бергамотом, мммм, вкусненько.")
    time.sleep(1)
    await callback_query.answer("🗣 Но моя дудка села, а в магазин за сигами идти не хочу.\nТам сегодня одна не очень нормальная работает.\nНе люблю её.")
    time.sleep(1)
    await callback_query.answer("🗣 Короче, стрельнишь сигу?\nКосарь дам, мне для сестрички ничего не жалко.")
    time.sleep(1)
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🚬 Угостить человечка сигареткой 🚬",
                    callback_data="cigarette")
    keyboard.button(text="🙅‍♀️ Нафиг этого прокурыша недоделанного 🙅‍♀️",
                    callback_data=f"npc_{npc_id}")
    keyboard.adjust(1)

    await callback_query.answer("Что делать будем?", reply_markup=keyboard.as_markup())


async def cigarette(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик выдачи сигарет.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    other_items = get_user_data("other_items", user_id)
    cigarette = other_items.get('Сигареты', 0)
    keyboard = InlineKeyboardBuilder()
    if cigarette > 0:
        other_items['Сигареты'] = cigarette - 1
        update_user_data("other_items", other_items, user_id)
        await callback_query.answer("🗣 Спасибки, родная, спасибки, двуглазка\nИхихихихихихихихихи\n\nТы буквально спасла мою пропащую зависимую душу.")
        time.sleep(1)
        await callback_query.answer("🗣 Сколько я там тебе обещал? Косарь?\nВот, держи.\nГлавное сама не кури - это вредно. ")
        keyboard.button(text="💵 Взять money и гордиться собой 💵",
                        callback_data="money_1000_Cigarette")
    else:
        await callback_query.answer(f"🗣 Ну что там? Будет какой-нибудь никотин?")
        time.sleep(1)
        await callback_query.answer(f"🗣 Приходи ко мне, когда будет чем угостить, а не только поиздеваться.")
        keyboard.button(text="🙁 Идти гулять и искать сиги 🙁",
                        callback_data="to_do")
        time.sleep(1)
    await callback_query.answer("Выбора нет, надо тыкать на кнопочку ниже:", reply_markup=keyboard.as_markup())


async def quest_quiz(callback_query: CallbackQuery, npc_id: int, user_id: int) -> None:
    """
    Обработчик квиза на знание алкогольных напитков от NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - npc_id: ID NPC.
    - user_id: ID пользователя.
    """
    await callback_query.answer("🗣 Добрый вечер, я диспетчер!")
    time.sleep(1)
    await callback_query.answer("🗣 На самом деле я профессор философии.\nНе веришь?\nДа я тебе отвечаююю.")
    time.sleep(1)
    await callback_query.answer("🗣 Короче, сейчас объектом моих глубинный размышлений является важность алкоголя у смертных.")
    time.sleep(1)
    await callback_query.answer("🗣 Не мог бы ты мне помочь мне?\nНу там просто поотвечать на вопросики?\nТы не бойся, там не философские вопросы, там такие, культурно-спиртные.")
    time.sleep(1)
    await callback_query.answer("🗣 Ну и естественно, я плачу за свои исследовательские приколы. Могу коктейличик тебе за помощь купить, могу деньгами отдать.")
    time.sleep(1)
    await callback_query.answer("🗣 Ну что? Поможешь?\nТолько учти, что одна ошибка и квиз надо заново начинать.")
    time.sleep(1)
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🍷 Блеснуть своими алко-знаниями 🍷",
                    callback_data="quiz_1")
    keyboard.button(text="🙅‍♀️ Нафиг этого философа недоделанного 🙅‍♀️",
                    callback_data=f"npc_{npc_id}")
    keyboard.adjust(1)
    await callback_query.answer("Что делать будем?", reply_markup=keyboard.as_markup())


async def quiz_1(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик первого вопроса квиза на знание алкогольных напитков от NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    await callback_query.answer("🗣 Ну что ж, погнали, мой юный философ!")
    time.sleep(2)
    await callback_query.answer("🗣 Какой алкогольный напиток готовится из виноградного сока, который не был полностью ферментирован и оставляет сладкий вкус?")
    keyboard.button(text="Розовое вино", callback_data="false")
    keyboard.button(text="Ламбруско", callback_data="false")
    keyboard.button(text="Портвейн", callback_data="quiz_2")
    keyboard.button(text="Вермут", callback_data="false")
    keyboard.adjust(2)
    await callback_query.answer("Ваш выбор:", reply_markup=keyboard.as_markup())


async def quiz_2(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик второго вопроса квиза на знание алкогольных напитков от NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    await callback_query.answer("🗣 Конечно же это был портвейн - креплёное вино, производимое на северо-востоке Португалии в долине реки Дору!")
    time.sleep(1)
    await callback_query.answer("🗣 Какой из следующий спиртных напитков считается национальным напитком Бразилии?")
    keyboard.button(text="Писко", callback_data="false")
    keyboard.button(text="Текила", callback_data="false")
    keyboard.button(text="Самбука", callback_data="false")
    keyboard.button(text="Кашаса", callback_data="quiz_3")
    keyboard.adjust(2)
    await callback_query.answer("Ваш выбор:", reply_markup=keyboard.as_markup())


async def quiz_3(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик третьего вопроса квиза на знание алкогольных напитков от NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    await callback_query.answer("🗣 И это кашаса - крепкий алкогольный напиток, похож на ром, но первый делают из сахарного тросника, а второй чаще всего из патоки.")
    time.sleep(1)
    await callback_query.answer("🗣 Какой из следующий ликеров имеет характерный вкус меда и трав?")
    keyboard.button(text="Драмбуи", callback_data="quiz_4")
    keyboard.button(text="Амаретто", callback_data="false")
    keyboard.button(text="Куантро", callback_data="false")
    keyboard.button(text="Блю кюрасао", callback_data="false")
    keyboard.adjust(2)
    await callback_query.answer("Ваш выбор:", reply_markup=keyboard.as_markup())


async def quiz_4(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик четвертого вопроса квиза на знание алкогольных напитков от NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    await callback_query.answer("🗣 Драмбу́и — ликёр, приготовленный из выдержанного шотландского виски с ароматом мёда, "
                                "аниса, шафрана, мускатного ореха и различных трав.")
    time.sleep(1)
    await callback_query.answer("🗣 Какой из следующий коктейлей традиционно включает текилу, ликер Трипл Сек и лаймовый сок?")
    keyboard.button(text="Маргарита", callback_data="quiz_5")
    keyboard.button(text="Лонг-Айленд", callback_data="false")
    keyboard.button(text="Дайкири", callback_data="false")
    keyboard.button(text="Май Тай", callback_data="false")
    keyboard.adjust(2)
    await callback_query.answer("Ваш выбор:", reply_markup=keyboard.as_markup())


async def quiz_5(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик пятого вопроса квиза на знание алкогольных напитков от NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    await callback_query.answer("🗣 Ну конечно же это - Маргарита! "
                                "В самой популярной версии авторство принадлежит светской львице Маргарите Сеймз. "
                                "По легенде, она смешала коктейль из текилы, апельсинового ликера и лаймового сока "
                                "для гостей своей вечеринки в Акапулько в конце 40-х.")
    time.sleep(1)
    await callback_query.answer("🗣 Как называется теника смешивания, при которой ингредиенты добавляют по очереди, "
                                "не перемегивая их, чтобы создать слои у коктейлей?")
    keyboard.button(text="Стир", callback_data="false")
    keyboard.button(text="Шейк", callback_data="false")
    keyboard.button(text="Флоат", callback_data="quiz_6")
    keyboard.button(text="Билд", callback_data="false")
    keyboard.adjust(2)
    await callback_query.answer("Ваш выбор:", reply_markup=keyboard.as_markup())


async def quiz_6(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик шестого вопроса квиза на знание алкогольных напитков от NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    await callback_query.answer("🗣 И это метод флоат. Таким методом, например, делают коктейли Б-52 или Хирасиму.")
    time.sleep(1)
    await callback_query.answer("🗣 Что из перечисленного является основным ингредиентом самбуки?")
    keyboard.button(text="Полынь", callback_data="false")
    keyboard.button(text="Пшеница", callback_data="false")
    keyboard.button(text="Агава", callback_data="false")
    keyboard.button(text="Анис", callback_data="quiz_7")
    keyboard.adjust(2)
    await callback_query.answer("Ваш выбор:", reply_markup=keyboard.as_markup())


async def quiz_7(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик седьмого вопроса квиза на знание алкогольных напитков от NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    await callback_query.answer("🗣 Самбу́ка — итальянский ликёр с ароматом аниса, крепостью от 38% до 42%."
                                "Вырабатывается из экстракта аниса звёздчатого, и в отличие от других хорошо известных анисовых крепких напитков,"
                                "особую сбалансированность вкуса, самбуке придает еще один ингредиент – масло бузины.")
    time.sleep(1)
    await callback_query.answer("🗣 Из какого сорта винограда чаще всего делают вино?")
    keyboard.button(text="Каберне Совиньон", callback_data="quiz_8")
    keyboard.button(text="Шардоне", callback_data="false")
    keyboard.button(text="Мерло", callback_data="false")
    keyboard.button(text="Пино Нуар", callback_data="false")
    keyboard.adjust(2)
    await callback_query.answer("Ваш выбор:", reply_markup=keyboard.as_markup())


async def quiz_8(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик восьмого вопроса квиза на знание алкогольных напитков от NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    await callback_query.answer("🗣 Каберне Совиньон обладает насыщенным вкусом с нотками черной смородины, черешни и зеленого перца,"
                                "высокой танинностью и потенциалом для долгой выдержки.")
    time.sleep(1)
    await callback_query.answer("🗣 Из чего делают скотч?")
    keyboard.button(text="Рожь", callback_data="false")
    keyboard.button(text="Пшеница", callback_data="false")
    keyboard.button(text="Ячмень", callback_data="quiz_9")
    keyboard.button(text="Кукуруза", callback_data="false")
    keyboard.adjust(2)
    await callback_query.answer("Ваш выбор:", reply_markup=keyboard.as_markup())


async def quiz_9(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик девятого вопроса квиза на знание алкогольных напитков от NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    await callback_query.answer("🗣 Хотя и рожь, и пшеница, и кукуруза являются ингредиентами виски, в основе скотча (шотландского виски) преобладает ячмень.")
    time.sleep(1)
    await callback_query.answer("🗣 Из какого фрукта нельзя сделать сидр?")
    keyboard.button(text="Вишня", callback_data="false")
    keyboard.button(text="Виноград", callback_data="quiz_10")
    keyboard.button(text="Груша", callback_data="false")
    keyboard.button(text="Персик", callback_data="false")
    keyboard.adjust(2)
    await callback_query.answer("Ваш выбор:", reply_markup=keyboard.as_markup())


async def quiz_10(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик десятого вопроса квиза на знание алкогольных напитков от NPC.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    await callback_query.answer("🗣 Если мы попробуем сделать сидр из винограда, мы получим вино. Упссс.")
    time.sleep(1)
    await callback_query.answer("🗣 Какой из следующий алкогольных напитков не является бренди?")
    keyboard.button(text="Коньяк", callback_data="false")
    keyboard.button(text="Арманьяк", callback_data="false")
    keyboard.button(text="Ром", callback_data="quiz_finish")
    keyboard.button(text="Кальвадос", callback_data="false")
    keyboard.adjust(2)
    await callback_query.answer("Ваш выбор:", reply_markup=keyboard.as_markup())


async def quiz_finish(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик завершения квиза при правильных ответах.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    await callback_query.answer("🗣 Бренди - это алкогольный напиток, производимый из дистиллированного виноградного вина, который часто выдерживается в дубовых бочках."
                                "Разновидностей бренди, как видишь, бывает мног.")
    await callback_query.answer("🗣 Обалдеть, ты прошел весь тест.\n\nДаже интересно, с какой попытки?\nАхахахахахахаах")
    await callback_query.answer("🗣 Поздравляю, друг мой эрудированный, ты настоящий алко-знаток.\nЗа такой успех кину тебе на карту тыщи 2.")
    keyboard.button(text="💵 Взять money и гордиться собой 💵",
                    callback_data="money_2000_Quiz")
    await callback_query.answer("Выбора нет, надо тыкать на кнопочку ниже:", reply_markup=keyboard.as_markup())


async def quiz_false(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Обработчик завершения квиза при неправильных ответах.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    await callback_query.answer("🗣 Ну что ж, мой друг, тебе не повезло, придется начать всё заново((")
    keyboard.button(text="🐣 Начать занаво 🐣", callback_data="quiz_1")
    keyboard.button(text="🙅‍♀️ Нафиг этот квиз, ухожу 🙅‍♀️",
                    callback_data="to_do")
    await callback_query.answer("Вот она - философская проблема выбора:", reply_markup=keyboard.as_markup())


async def get_money(callback_query: CallbackQuery, data: str, user_id: int) -> None:
    """
    Обработчик получения денег после выполнения квеста.
    Параметры:
    - callback_query: Объект callback_query.
    - data: Данные из callback_data.
    - user_id: ID пользователя.
    """
    data_parts = data.split('_')
    get_money = int(data_parts[1])
    quest_name = data_parts[2]
    now_money = get_user_data("money", user_id)
    update_user_data("money", now_money + get_money, user_id)
    update_quest_data("done", 1, quest_name, user_id)
    npc_id = get_npc_data(user_id, quest_name)
    update_npc_data("quest_done", 1, npc_id)
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🕺 Let's go тусить дальше 🕺", callback_data="to_do")
    await callback_query.answer(f"Урааааа, теперь у нас на счету {now_money + get_money} монеток", reply_markup=keyboard.as_markup())
