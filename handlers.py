import json
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

import keyboard as kb
from calendar_myad import recount as money_recount, configjson
from dfs import push_to_json, take_from_json, take_balance


class Add(StatesGroup):
    name = State()
    price = State()


class Substruct(StatesGroup):
    name = State()
    price = State()

class Addnew(StatesGroup):
    name = State()
    price = State()

class Delete(StatesGroup):
    name = State()

router = Router()

add_json_to_push = {}
sub_json_to_push = {}
in_sub_edit = False
in_add_edit = False

config_json = take_from_json("config.json")


@router.message(CommandStart())
async def start(message: Message):
    global config_json
    config_json = take_from_json("config.json")
    if message.from_user.id in config_json["ids"]:
        await message.answer('Привет\nНапиши /help чтобы получить полный список команд',
                             reply_markup=kb.maink)


@router.message(Command('help'))
async def get_help(message: Message):
    global config_json
    config_json = take_from_json("config.json")
    if message.from_user.id in config_json["ids"]:
        await message.answer("Команды:\n/add - Оплата ученика;\n/sub - Вычесть сумму вручную\n/addnew - добавить нового ученика\n/del - Удалить ученика\n/check - проверить електронный баланс")


@router.message(F.text == "Пересчитать babosiki")
async def recount(message: Message):
    global config_json
    config_json = take_from_json("config.json")
    if message.from_user.id in config_json["ids"]:
        errors = money_recount()
        money = take_from_json(config_json["moneycount"])
        stringa = take_balance(money)
        await message.answer(stringa)
        if errors != '':
            await message.answer(f'Ошибки:\n{errors}')


@router.message(Command("add"))
async def addmoney(message: Message, state: FSMContext):
    global config_json
    config_json = take_from_json("config.json")
    if message.from_user.id in config_json["ids"]:
        await state.set_state(Add.name)
        stringa = 'Выбери одного:\n'
        babosiki = take_from_json(config_json["moneycount"])
        for i in babosiki:
            stringa += f'`{i}`\n'
        stringa += '\nВыберите и пришлите 1 из этих учеников'
        await message.answer(stringa,
                             parse_mode="MARKDOWN")


@router.message(Add.name)
async def getname(message: Message, state: FSMContext):
    if message.from_user.id in config_json["ids"]:
        data = take_from_json(config_json["moneycount"])
        if message.text not in data:
            await message.answer('нету такого')
            await state.clear()
            return
        await state.update_data(name=message.text)
        await state.set_state(Add.price)
        await message.answer('Теперь пришлите сколько оплачено denyzhek)))')


@router.message(Add.price)
async def get_price(message: Message, state: FSMContext):
    # ДОБАВЛЮ ПОТОМ ВОЗМОЖНОСТЬ РЕДАКТИРОВАТЬ И ВСЯ ФИГНЯВАЧКА
    global in_add_edit, add_json_to_push
    if message.from_user.id in config_json["ids"]:
        if not message.text.isnumeric():
            await message.answer('Неправильный ввод\nначните заного - /addnew')
            await state.clear()
            return
        await state.update_data(price=message.text)
        data = await state.get_data()
        dat = take_from_json(config_json["moneycount"])
        dat[data["name"]] += int(data["price"])
        await state.clear()
        add_json_to_push = dat
        in_add_edit = True
        await message.answer(text=f'Имя: {data["name"]}\nСумма: {data["price"]}',
                             reply_markup=kb.Addedit)


@router.callback_query(F.data == 'addok')
async def add_ok(callback: CallbackQuery):
    global in_add_edit
    if in_add_edit:
        await callback.message.edit_text(text='Успешно!',
                                         reply_markup=None)
        in_add_edit = False
        push_to_json(config_json["moneycount"], add_json_to_push)


@router.message(Command('sub'))
async def sub_struct(message: Message, state: FSMContext):
    global config_json
    config_json = take_from_json("config.json")
    if message.from_user.id in config_json["ids"]:
        await state.set_state(Substruct.name)
        stringa = 'Выбери одного:\n'
        babosiki = take_from_json(config_json["moneycount"])
        for i in babosiki:
            stringa += f'`{i}`\n'
        stringa += '\nВыберите и пришлите 1 из этих учеников'
        await message.answer(stringa,
                             parse_mode="MARKDOWN")


@router.message(Substruct.name)
async def Sub_name(message: Message, state: FSMContext):
    if message.from_user.id in config_json["ids"]:
        data = take_from_json(config_json["moneycount"])
        if message.text not in data:
            await message.answer('нету такого')
            await state.clear()
            return
    await state.update_data(name=message.text)
    await state.set_state(Substruct.price)
    await message.answer('Теперь пришлите сколько нужно вычесть')


@router.message(Substruct.price)
async def Sub_price(message: Message, state: FSMContext):
    global sub_json_to_push, in_sub_edit
    if message.from_user.id in config_json["ids"]:
        await state.update_data(price=message.text)
        data = await state.get_data()
        dat = take_from_json(config_json["moneycount"])
        dat[data["name"]] -= int(data["price"])
        sub_json_to_push = dat
        in_sub_edit = True
        await state.clear()
        await message.answer(text=f'Имя: {data["name"]}\nСумма вычета: {data["price"]}',
                             reply_markup=kb.Subedit)


@router.callback_query(F.data == 'subok')
async def subok(callback: CallbackQuery):
    global sub_json_to_push, in_sub_edit
    if in_sub_edit:
        await callback.message.edit_text(text='Успешно!',
                                         reply_markup=None)
        in_sub_edit = False
        push_to_json(config_json["moneycount"], sub_json_to_push)


@router.callback_query(F.data == 'wrong')
async def wrong(callback: CallbackQuery):
    await callback.message.delete()
    global in_sub_edit, in_add_edit
    await callback.message.answer(text='Начать заного - /sub или /add')
    in_sub_edit = False
    in_add_edit = False


@router.message(Command('addnew'))
async def add_new(message: Message, state: FSMContext):
    config_json = take_from_json("config.json")
    if message.from_user.id in config_json["ids"]:
        await state.set_state(Addnew.name)
        await message.answer('Введите имя ученика:')

@router.message(Addnew.name)
async def add_new_name(message: Message, state: FSMContext):
    if message.from_user.id in config_json["ids"]:
        await state.update_data(name = message.text)
        await state.set_state(Addnew.price)
        await message.answer('Пришлите баланс ученика:')

@router.message(Addnew.price)
async def add_new_price(message: Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.answer('Неправильный ввод\nначните заного - /addnew')
        await state.clear()
        return
    await state.update_data(price=int(message.text))
    add_new_json = take_from_json(config_json["moneycount"])
    data = await state.get_data()
    add_new_json[data["name"]] = data["price"]
    push_to_json(config_json["moneycount"], add_new_json)
    await state.clear()
    await message.answer("Успешно!")


@router.message(Command('del'))
async def delete(message: Message, state: FSMContext):
    config_json = take_from_json("config.json")
    if message.from_user.id in config_json["ids"]:
        await state.set_state(Delete.name)
        stringa = 'Выбери одного:\n'
        babosiki = take_from_json(config_json["moneycount"])
        for i in babosiki:
            stringa += f'`{i}`\n'
        stringa += '\nВыберите и пришлите 1 из этих учеников'
        await message.answer(stringa,
                             parse_mode="MARKDOWN")

@router.message(Delete.name)
async def delete_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    delete_json = take_from_json(config_json["moneycount"])
    if message.text not in delete_json:
        await message.answer('Нету такого\nЗаного - /del')
        await state.clear()
        return
    delete_json.pop(message.text)
    push_to_json(config_json["moneycount"], delete_json)
    await message.answer('Успешно!')
    await state.clear()

@router.message(Command('check'))
async def balance(message: Message):
    config_json = take_from_json("config.json")
    if message.from_user.id in config_json["ids"]:
        money = take_from_json(config_json["moneycount"])
        stringa = take_balance(money)
        await message.answer(stringa)
