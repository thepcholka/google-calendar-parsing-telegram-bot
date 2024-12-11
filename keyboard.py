from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

maink = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="💰💰💰Пересчитать babosiki💰💰💰")],
    [KeyboardButton(text="/add"), KeyboardButton(text='/sub')]
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
