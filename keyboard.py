from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

maink = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Пересчитать babosiki"), KeyboardButton(text='/check')],
    [KeyboardButton(text="/add"), KeyboardButton(text='/sub')],
    [KeyboardButton(text='/addnew'), KeyboardButton(text='/del')]
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

Addnew = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text='Да', callback_data='yes'), InlineKeyboardButton(text="Нет", callback_data='no')]
])