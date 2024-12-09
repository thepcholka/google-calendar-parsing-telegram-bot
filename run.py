import asyncio
import logging
import json
from aiogram import Dispatcher, Bot
from handlers import router

with open("config.json") as file:
    config = json.load(file)
Token = config["Token"]

bot = Bot(token=Token)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="lenglogs", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')