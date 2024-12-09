import json
from run import bot

def takefromjson(json_name):
    with open(json_name) as jsonfil:
        jsonfile = json.load(jsonfil)
    return jsonfile

configjson = takefromjson("config.json")

async def senderror(message):
    await bot.send_message(configjson["mainadmin"], text=f'ОШИБКА: {message}')
