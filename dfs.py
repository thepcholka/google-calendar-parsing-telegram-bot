import json

def push_to_json(json_name, file_to_push):
    with open(json_name, "w") as jsonfile:
        json.dump(file_to_push, jsonfile)

def take_from_json(json_name):
    with open(json_name) as jsonfil:
        jsonfile = json.load(jsonfil)
    return jsonfile

def take_balance(money):
    stringa = ''
    for i in money:
        if money[i] < 0:
            stringa += f'Долг {i} равен: {money[i]} руб\n'
        elif money[i] >= 0:
            stringa += f'Остаток {i} равен: {money[i]} руб\n'
    return stringa