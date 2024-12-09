import asyncio
import datetime
import json
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiohttp.web_routedef import route
from defs import pushtojson, takefromjson
import keyboard as kb
from calendar_myad import recount as money_recount

router = Router()

class Add(StatesGroup):
    name = State()
    price = State()
class Substruct(StatesGroup):
    name = State()
    price = State()


addjsontopush = {}
subjsontopush = {}
insubedit = False
inaddedit = False

configjson = takefromjson("config.json")
admin_ids = configjson["ids"]

@router.message(CommandStart())
async def start(message: Message):
    if message.from_user.id in admin_ids:
        if message.from_user.id in configjson["ids"]:
            await message.answer('Привет\nНапиши /help чтобы получить полный список команд',
                         reply_markup= kb.maink)

@router.message(Command('help'))
async def get_help(message: Message):
    if message.from_user.id in admin_ids:
        await message.answer("Команды: /add - Оплата ученика; /sub - Вычесть сумму вручную")


@router.message(F.text == "💰💰💰Пересчитать babosiki💰💰💰")
async def recount (message: Message):
    if message.from_user.id in admin_ids:
        money_recount()
        with open("babkibabkisukababki.json") as file:
            money = json.load(file)
        for i in money:
            if money[i] < 0:
                await message.answer(f'Долг {i} равен: {money[i]}')
            elif money[i] >= 0:
                await message.answer(f'Остаток {i} равен: {money[i]}')


@router.message(Command("add"))
async def addmoney(message: Message, state: FSMContext):
    if message.from_user.id in admin_ids:
        await state.set_state(Add.name)
        stringa = 'Выбери одного:\n'
        babosiki = takefromjson(configjson["moneycount"])
        for i in babosiki:
            stringa += f'`{i}`\n'
        stringa += '\nВыберите и пришлите 1 из этих учеников'
        await message.answer(stringa,
                       parse_mode="MARKDOWN")

@router.message(Add.name)
async def getname(message: Message, state: FSMContext):
    if message.from_user.id in admin_ids:
        data = takefromjson(configjson["moneycount"])
        if message.text not in data:
            await message.answer('нету такого')
            await state.clear()
            return
        await state.update_data(name = message.text)
        await state.set_state(Add.price)
        await message.answer('Теперь пришлите сколько оплачено denyzhek)))')

@router.message(Add.price)
async def getprice(message: Message, state: FSMContext):
#ДОБАВЛЮ ПОТОМ ВОЗМОЖНОСТЬ РЕДАКТИРОВАТЬ И ВСЯ ФИГНЯВАЧКА
    global inaddedit
    if message.from_user.id in admin_ids:
        await state.update_data(price = message.text)
        data = await state.get_data()
        dat = takefromjson(configjson["moneycount"])
        dat[data["name"]] += int(data["price"])
        inaddedit = True
        await message.answer(text=f'Имя: {data["name"]}\nСумма вычета: {data["price"]}',
                             reply_markup=kb.Addedit)

@router.callback_query(F.data == 'addok')
async def addok(callback : CallbackQuery):
    global inaddedit, addjsontopush
    if inaddedit:
        inaddedit = False
        pushtojson(addjsontopush, configjson["moneycount"])

@router.message(Command('sub'))
async def substruct(message: Message, state: FSMContext):
    if message.from_user.id in admin_ids:
        await state.set_state(Substruct.name)
        stringa = 'Выбери одного:\n'
        babosiki = takefromjson(configjson["moneycount"])
        for i in babosiki:
            stringa += f'`{i}`\n'
        stringa += '\nВыберите и пришлите 1 из этих учеников'
        await message.answer(stringa,
                             parse_mode="MARKDOWN")

@router.message(Substruct.name)
async def Subname(message : Message, state : FSMContext):
    if message.from_user.id in admin_ids:
        data = takefromjson(configjson["moneycount"])
        if message.text not in data:
            await message.answer('нету такого')
            await state.clear()
            return
    await state.update_data(name=message.text)
    await state.set_state(Substruct.price)
    await message.answer('Теперь пришлите сколько нужно вычесть')

@router.message(Substruct.price)
async def Subprice(message : Message, state : FSMContext):
    global subjsontopush, insubedit
    if message.from_user.id in admin_ids:
        await state.update_data(price = message.text)
        data = await state.get_data()
        dat = takefromjson(configjson["moneycount"])
        dat[data["name"]] -= int(data["price"])
        subjsontopush = dat
        await state.clear()
        await message.answer(text=f'Имя: {data["name"]}\nСумма вычета: {data["price"]}',
                             reply_markup= kb.Subedit)

@router.callback_query(F.data == 'subok')
async def subok(callback : CallbackQuery):
    global subjsontopush, insubedit
    if insubedit:
        insubedit = False
        pushtojson(subjsontopush, configjson["moneycount"])

@router.callback_query(F.data == 'wrong')
async def wrong(callback : CallbackQuery):
    global insubedit, inaddedit
    await callback.message.answer(text='Начать заного - /sub или /add')
    insubedit = False
    inaddedit = False