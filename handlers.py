import datetime
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiohttp.web_routedef import route
import asyncio
import json

from calendar_myad import main1 as shet
import keyboard as kb
router = Router()
class Ad(StatesGroup):
    name = State()
    price = State()

with open("config.json") as file:
    config = json.load(file)
@router.message(CommandStart())
async def start(message: Message):
    if message.from_user.id in config["ids"]:
        await message.answer('Привет\nНапиши /help чтобы получить полный список команд',
                         reply_markup= kb.maink)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer("Команды: /add - Оплата ученика")


@router.message(F.text == "💰💰💰Пересчитать babosiki💰💰💰")
async def pereschet(message: Message):
    shet()
    with open("babkibabkisukababki.json") as file:
        money = json.load(file)
    stringa = ''
    for i in money:
        stringa += f'Счет {i}: ({money[i]})\n'
    await message.answer(text=stringa)

@router.message(Command("add"))
async def addmoney(message: Message, state: FSMContext):
    await state.set_state(Ad.name)
    stringa = 'Выбери одного:\n'
    with open("babkibabkisukababki.json") as file:
        babosiki = json.load(file)
    for i in babosiki:
        stringa += f'`{i}`\n'
    stringa += '\nВыберите и пришлите 1 из этих учеников'
    await message.answer(stringa,
                   parse_mode="MARKDOWN")

@router.message(Ad.name)
async def getname(message: Message, state: FSMContext):
    with open("babkibabkisukababki.json") as file:
        data = json.load(file)
        if message.text not in data:
            await message.answer('нету такого')
            await state.clear()
            return
    await state.update_data(name = message.text)
    await state.set_state(Ad.price)
    await message.answer('Теперь пришлите сколько оплачено denyzhek)))')

@router.message(Ad.price)
async def getprice(message: Message, state: FSMContext):
#ДОБАВЛЮ ПОТОМ ВОЗМОЖНОСТЬ РЕДАКТИРОВАТЬ И ВСЯ ФИГНЯВАЧКА
    await state.update_data(price = message.text)
    data = await state.get_data()
    with open("babkibabkisukababki.json") as file:
        dat = json.load(file)
    dat[data["name"]] += int(data["price"])
    with open("babkibabkisukababki.json", "w") as fil:
        json.dump(dat, fil)
    await state.clear()
