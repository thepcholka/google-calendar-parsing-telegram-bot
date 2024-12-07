import asyncio
import logging
import json

with open("config.json") as file:
    config = json.load(file)
Token = config["Token"]
from aiogram import Dispatcher, Bot
from handlers import router
bot = Bot(token=Token)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')