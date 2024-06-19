from aiogram import types
from aiogram import Dispatcher, types
from aiogram.filters import Command

from . import quest, npc, info_inventory, location, main_buttons, menu, enemy


dp = Dispatcher()
user_states = {}


async def check_user_states(message: types.Message, func, user_id=None):
    if user_states.get(message.from_user.id, "OK") != "awaiting_dice":
        await func(message, user_id) if user_id else await func(message)
    else:
        await message.answer("Ахахахахахахахаха\n"
                             "Нифига подобного, сначала пей, а потом иди куда хочешь.\n"
                             "А ну быстро иди бросать кубик ⬆️")


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await check_user_states(message, menu.send_welcome)


@dp.message(Command("info"))
async def send_info(message: types.Message):
    user_id = message.from_user.id
    await check_user_states(message, menu.send_info, user_id)


@dp.message(Command("inventory"))
async def send_inventory(message: types.Message):
    user_id = message.from_user.id
    await check_user_states(message, menu.send_inventory, user_id)


@dp.message(Command("location"))
async def send_location(message: types.Message):
    user_id = message.from_user.id
    await check_user_states(message, menu.send_location, user_id)


@dp.message(Command("scheme"))
async def send_scheme(message: types.Message):
    user_id = message.from_user.id
    await check_user_states(message, menu.send_scheme, user_id)


@dp.message(Command("characters"))
async def send_characters(message: types.Message):
    user_id = message.from_user.id
    await check_user_states(message, menu.send_characters, user_id)


@dp.message(Command("new_game"))
async def new_game(message: types.Message):
    await check_user_states(message, menu.new_game)


@dp.message(Command("rules"))
async def send_rules(message: types.Message):
    await check_user_states(message, menu.send_rules)


async def send_main_menu_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await main_buttons.send_main_menu(call.message, user_id)


async def to_do_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await main_buttons.to_do(call.message, user_id)


async def new_game_yes_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await menu.new_game_yes(call.message, user_id)


async def send_info_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await menu.send_info(call.message, user_id)


async def my_snail_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await info_inventory.my_snail(call.message, user_id)


async def send_inventory_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await menu.send_inventory(call.message, user_id)


async def send_inventory_type_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await info_inventory.send_inventory_type(call.message, user_id, call.data)


async def send_location_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await menu.send_location(call.message, user_id)


async def move_location_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await location.move_location(call.message, user_id)


async def go_to_new_location_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await location.go_to_new_location(call.message, user_id, call.data)


async def send_characters_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await menu.send_characters(call.message, user_id)


async def choose_npc_to_talk_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await npc.choose_npc_to_talk(call.message, call.data, user_id)


async def talk_to_npc_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await npc.talk_to_npc(call.message, call.data, user_id)


async def choose_enemy_to_talk_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await enemy.choose_enemy_to_talk(call.message, call.data, user_id)


async def talk_to_enemy_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await enemy.talk_to_enemy(call.message, call.data, user_id)


async def drink_enemy_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await enemy.drink_enemy(call.message, call.data, user_id)


async def drink_snail_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await enemy.drink_snail(call.message, call.data, user_id)


async def winner_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await enemy.winner(call.message, user_id)


async def anti_winner_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await enemy.anti_winner(call.message, user_id)


async def bar_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.bar(call.message, user_id)


async def photographer_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.photographer(call.message, user_id)


async def recipe_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.recipe(call.message, user_id)


async def cigarette_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.cigarette(call.message, user_id)


async def quiz_1_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.quiz_1(call.message, user_id)


async def quiz_2_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.quiz_2(call.message, user_id)


async def quiz_3_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.quiz_3(call.message, user_id)


async def quiz_4_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.quiz_4(call.message, user_id)


async def quiz_5_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.quiz_5(call.message, user_id)


async def quiz_6_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.quiz_6(call.message, user_id)


async def quiz_7_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.quiz_7(call.message, user_id)


async def quiz_8_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.quiz_8(call.message, user_id)


async def quiz_9_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.quiz_9(call.message, user_id)


async def quiz_10_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.quiz_10(call.message, user_id)


async def quiz_finish_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.quiz_finish(call.message, user_id)


async def quiz_false_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.quiz_false(call.message, user_id)


async def get_money_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await quest.get_money(call.message, call.data, user_id)


async def find_fun_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await location.find_fun(call.message, user_id)


async def use_toilet_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_name = call.from_user.full_name
    await location.use_toilet(call.message, user_id, user_name)


async def use_roof_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await location.use_roof(call.message, user_id)


async def use_hall_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await location.use_hall(call.message, user_id)


async def use_market_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await location.use_market(call.message, user_id)


async def buy_market_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await location.buy_market(call.message, call.data, user_id)


async def pay_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    await location.pay(call.message, call.data, user_id)


dp.callback_query(lambda call: call.data == 'send_main_menu')(
    send_main_menu_callback)
dp.callback_query(lambda call: call.data == 'to_do')(to_do_callback)
dp.callback_query(lambda call: call.data ==
                  'new_game_yes')(new_game_yes_callback)

dp.callback_query(lambda call: call.data == 'info')(send_info_callback)
dp.callback_query(lambda call: call.data == 'my_snail')(my_snail_callback)
dp.callback_query(lambda call: call.data == 'inventory')(
    send_inventory_callback)
dp.callback_query(lambda call: call.data.startswith(
    'inventory_'))(send_inventory_type_callback)

dp.callback_query(lambda call: call.data == 'location')(send_location_callback)
dp.callback_query(lambda call: call.data.startswith('move'))(
    move_location_callback)
dp.callback_query(lambda call: call.data.startswith('go_'))(
    go_to_new_location_callback)

dp.callback_query(lambda call: call.data == 'characters')(
    send_characters_callback)
dp.callback_query(lambda call: call.data.startswith('npc_'))(
    choose_npc_to_talk_callback)
dp.callback_query(lambda call: call.data.startswith(
    'talknpc_'))(talk_to_npc_callback)

dp.callback_query(lambda call: call.data.startswith(
    'enemy_'))(choose_enemy_to_talk_callback)
dp.callback_query(lambda call: call.data.startswith(
    'talkenemy_'))(talk_to_enemy_callback)
dp.callback_query(lambda call: call.data.startswith(
    'drinkenemy_'))(drink_enemy_callback)
dp.callback_query(lambda call: call.data.startswith(
    'drinksnail_'))(drink_snail_callback)
dp.callback_query(lambda call: call.data.startswith('winner'))(winner_callback)
dp.callback_query(lambda call: call.data.startswith(
    'anti_winner'))(anti_winner_callback)

dp.callback_query(lambda call: call.data == 'bar')(bar_callback)
dp.callback_query(lambda call: call.data ==
                  'photographer')(photographer_callback)
dp.callback_query(lambda call: call.data == 'recipe')(recipe_callback)
dp.callback_query(lambda call: call.data == 'cigarette')(cigarette_callback)
dp.callback_query(lambda call: call.data == 'quiz_1')(quiz_1_callback)
dp.callback_query(lambda call: call.data == 'quiz_2')(quiz_2_callback)
dp.callback_query(lambda call: call.data == 'quiz_3')(quiz_3_callback)
dp.callback_query(lambda call: call.data == 'quiz_4')(quiz_4_callback)
dp.callback_query(lambda call: call.data == 'quiz_5')(quiz_5_callback)
dp.callback_query(lambda call: call.data == 'quiz_6')(quiz_6_callback)
dp.callback_query(lambda call: call.data == 'quiz_7')(quiz_7_callback)
dp.callback_query(lambda call: call.data == 'quiz_8')(quiz_8_callback)
dp.callback_query(lambda call: call.data == 'quiz_9')(quiz_9_callback)
dp.callback_query(lambda call: call.data == 'quiz_10')(quiz_10_callback)
dp.callback_query(lambda call: call.data ==
                  'quiz_finish')(quiz_finish_callback)
dp.callback_query(lambda call: call.data == 'false')(quiz_false_callback)
dp.callback_query(lambda call: call.data.startswith(
    'money_'))(get_money_callback)

dp.callback_query(lambda call: call.data == 'fun')(find_fun_callback)
dp.callback_query(lambda call: call.data == 'toilet')(use_toilet_callback)
dp.callback_query(lambda call: call.data == 'roof')(use_roof_callback)
dp.callback_query(lambda call: call.data == 'selfie')(use_hall_callback)
dp.callback_query(lambda call: call.data == 'market')(use_market_callback)
dp.callback_query(lambda call: call.data.startswith('buy_'))(
    buy_market_callback)
dp.callback_query(lambda call: call.data.startswith('pay_'))(pay_callback)
