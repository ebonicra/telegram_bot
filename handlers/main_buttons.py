from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from bot import bot


async def deactivate_buttons(obj: types.Message, chat_id: int, message_id: int) -> None:
    """
    Функция для деактивации предыдущих кнопок в сообщении.
    Параметры:
    - obj: Объект сообщения или callback_query.
    - chat_id: ID чата.
    - message_id: ID сообщения.
    """
    current_keyboard = obj.reply_markup
    inactive_keyboard = InlineKeyboardBuilder()
    if current_keyboard:
        for row in current_keyboard.inline_keyboard:
            new_row = []
            for button in row:
                new_row.append(InlineKeyboardButton(
                    text=button.text, callback_data="inactive"
                ))
            inactive_keyboard.row(*new_row)
        await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=inactive_keyboard.as_markup())


async def send_main_menu(message: types.Message, user_id: int) -> None:
    """
    Функция для отправки основного меню пользователю.
    Параметры:
    - message: Объект сообщения от пользователя.
    - user_id: ID пользователя.
    """
    await deactivate_buttons(message, user_id, message.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Кто я?", callback_data="info")
    keyboard.button(text="Где я?", callback_data="location")
    keyboard.button(text="Кто тут?", callback_data="characters")
    keyboard.adjust(1)
    await message.answer("Что будем делать?", reply_markup=keyboard.as_markup())


async def to_do(message: types.Message, user_id: int) -> None:
    """
    Функция для отправки меню с вариантами действий пользователю.
    Параметры:
    - message: Объект сообщения от пользователя.
    - user_id: ID пользователя.
    """
    await deactivate_buttons(message, user_id, message.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🕺 Пойдем куда-нибудь шататься", callback_data="move")
    keyboard.button(text="🐒 Будем изучать местную фауну",
                    callback_data="characters")
    keyboard.button(text="🧐 Может тут есть чё интересного?",
                    callback_data="fun")
    keyboard.button(text="🌚 Вот бы вспомнить, кто я такой?",
                    callback_data="my_snail")
    keyboard.adjust(1)
    await message.answer("Перфект, перфект\nТуц-туц\nПерфект, перфект\nТуц-туц\n\nНу и чё мы здесь будем делать?", reply_markup=keyboard.as_markup())
