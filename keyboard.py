from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

maink = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="💰💰💰Пересчитать babosiki💰💰💰")]
],
    resize_keyboard=True
                            )
Addedit = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text='Заново давай', callback_data = 'wrong')],
    [InlineKeyboardButton(text='Все ок', callback_data= 'addok')]
])
Subedit = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text='Заново давай', callback_data = 'wrong')],
    [InlineKeyboardButton(text='Все ок', callback_data='subok')]
])
