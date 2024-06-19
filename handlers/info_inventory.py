from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import time

from players_classes import Protagonist
from . import main_buttons


async def my_snail(callback_query: CallbackQuery, user_id: int) -> None:
    """
    Функция для отображения информации о персонаже (улитке).
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    """
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Что я за улитка такая?", callback_data="info")
    keyboard.button(text="Что у меня за душой?", callback_data="inventory")
    keyboard.button(text="⬅ Назад, плиз ⬅", callback_data="to_do")
    keyboard.adjust(1)
    response = ("Когда-нибудь у тебя будет хорошая память,\n"
                "Когда-нибудь будет светить голубое небо,\n"
                "Когда-нибудь это всё закончится.")
    await callback_query.answer(response)
    response = ("А пока тыкай и узнавай, что хотел.\n"
                "Я знаю всё про тебя.\n"
                "Только адреса не знаю.\n"
                "Так что такси заказвай себе сам.")
    await callback_query.answer(response, reply_markup=keyboard.as_markup())


async def send_inventory_type(callback_query: CallbackQuery, user_id: int, data: str) -> None:
    """
    Функция для отправки информации о типе инвентаря персонажа.
    Параметры:
    - callback_query: Объект callback_query.
    - user_id: ID пользователя.
    - data: Данные из callback_data (тип инвентаря).
    """
    type_inventory = data.split("_")[1]
    protagonist = Protagonist(user_id, 'default')
    snail = protagonist.send_inventory()
    if not snail:
        response = [
            "Твои карманы, также как и мозги - пусты. Нажми /start чтоб хоть что-то узнать."]
    else:
        response = protagonist.send_inventory_type(type_inventory)
    await callback_query.answer("Ты знал, что в среднем улитки живут 8 лет, "
                                "а пьющие и то меньше. Но что-то всё-таки ты успел приобрести. Удивительно.\n")
    for i in response:
        await callback_query.answer(i)
        time.sleep(1)
    await main_buttons.deactivate_buttons(callback_query, user_id, callback_query.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⬅ Назад, плиз ⬅", callback_data="inventory")
    await callback_query.answer("Горидись этим, нищеброд!", reply_markup=keyboard.as_markup())
