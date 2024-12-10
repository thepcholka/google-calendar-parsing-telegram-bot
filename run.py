import asyncio
import logging
import json
from aiogram import Dispatcher, Bot
from handlers import router
with open("config.json") as file:
    config = json.load(file)
Token = config["Token"]

dp = Dispatcher()
bot = Bot(token=Token)

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="lenglogs.txt", filemode="a",
                        format="%(asctime)s %(levelname)s %(message)s")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')