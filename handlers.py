import asyncio
import datetime
import json

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiohttp.web_routedef import route

from calendar_myad import main as money_recount
import keyboard as kb
router = Router()
class Add(StatesGroup):
    name = State()
    price = State()

with open("config.json") as file:
    config = json.load(file)
admin_ids = config["ids"]

@router.message(CommandStart())
async def start(message: Message):
    if message.from_user.id in admin_ids:
        if message.from_user.id in config["ids"]:
            await message.answer('Привет\nНапиши /help чтобы получить полный список команд',
                         reply_markup= kb.maink)

@router.message(Command('help'))
async def get_help(message: Message):
    if message.from_user.id in admin_ids:
        await message.answer("Команды: /add - Оплата ученика")


@router.message(F.text == "💰💰💰Пересчитать babosiki💰💰💰")
async def recount (message: Message):
    if message.from_user.id in admin_ids:
        money_recount()
        with open("babkibabkisukababki.json") as file:
            money = json.load(file)
        await message.answer('Индвидуальные ученики')
        for i in money["Ученики"]:
            if money["Ученики"][i] < 0:
                await message.answer(f'Долг {i} равен: {money["Ученики"][i]}')
            elif money["Ученики"][i] > 0:
                await message.answer(f'Остаток {i} равен: {money["Ученики"][i]}')
            else:
                await message.answer(f'{i} Красавчик, долг равен: {money["Ученики"][i]}')
        if len(money["Группы"]) != 0:
            await message.answer('Группы')
            for i in money["Группы"]:
                newgroup = ''
                for j in money["Группы"][i]:
                    if money["Группы"][i][j] < 0:
                        newgroup += f'Долг {j} равен: {money["Группы"][i][j]}\n'
                    elif money["Группы"][i][j] < 0:
                        newgroup += f'Остаток {j} равен: {money["Группы"][i][j]}\n'
                    else:
                        newgroup += f'{j} Красавчик, долг равен: {money["Группы"][i][j]}\n'
                await message.answer(f'Группа {money["Группа"][i]}\n{newgroup}')


@router.message(Command("add"))
async def addmoney(message: Message, state: FSMContext):
    if message.from_user.id in admin_ids:
        await state.set_state(Add.name)
        stringa = 'Выбери одного:\n'
        with open("babkibabkisukababki.json") as file:
            babosiki = json.load(file)
        for i in babosiki:
            stringa += f'`{i}`\n'
        stringa += '\nВыберите и пришлите 1 из этих учеников'
        await message.answer(stringa,
                       parse_mode="MARKDOWN")

@router.message(Add.name)
async def getname(message: Message, state: FSMContext):
    if message.from_user.id in admin_ids:
        with open("babkibabkisukababki.json") as file:
            data = json.load(file)
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
    if message.from_user.id in admin_ids:
        await state.update_data(price = message.text)
        data = await state.get_data()
        with open("babkibabkisukababki.json") as file:
            dat = json.load(file)
        dat[data["name"]] += int(data["price"])
        with open("babkibabkisukababki.json", "w") as fil:
            json.dump(dat, fil)
        await state.clear()
