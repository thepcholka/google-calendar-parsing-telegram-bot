import json
import logging
import os

def take_from_json(json_name):
    try:
        if os.path.exists(json_name) == False:
            logging.error(f'Файла с названием: ({json_name}) не существует')
        with open(json_name) as jsonfil:
            jsonfile = json.load(jsonfil)
        return jsonfile
    except:
        raise Exception(f'НЕВЕРНОЕ НАИМЕНОВАНИЕ ФАЙЛА: {json_name}')

def push_to_json(json_name, file_to_push, flag = 0):
    config_json =take_from_json("config.json")
    try:
        if os.path.exists(json_name) == False:
            logging.error(f'Файла с названием: ({json_name}) не существует')
        if flag == 1:
            with open(config_json["google_token"], "w") as token:
                token.write(file_to_push)
        with open(json_name, "w") as jsonfile:
            json.dump(file_to_push, jsonfile)
    except:
        raise Exception(f'НЕВЕРНОЕ НАИМЕНОВАНИЕ ФАЙЛА: {json_name}')


def take_balance(money):
    message_text = ''
    for i in money:
        if money[i] < 0:
            message_text += f'Долг {i} равен: {money[i]} руб\n'
        elif money[i] >= 0:
            message_text += f'Остаток {i} равен: {money[i]} руб\n'
    return message_text

