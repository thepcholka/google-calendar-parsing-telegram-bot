import asyncio
import logging
import json
from aiogram import Dispatcher, Bot, Router
with open("config.json") as file:
    config = json.load(file)
Token = config["Token"]

router = Router()
dp = Dispatcher()
bot = Bot(token=Token)

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="lenglogs.txt", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

async def senderror(message):
   await bot.send_message(config["mainadmin"], text=f'ОШИБКА: {message}')