from datetime import datetime
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
import logging
import os

def push_to_json(json_name, file_to_push, flag = 0):
    try:
        if os.path.exists(json_name) == False:
            logging.error(f'Файла с названием: ({json_name}) не существует')
        if flag == 1:
            with open("config.json", "w") as token:
                token.write(file_to_push)
        with open(json_name, "w") as jsonfile:
            json.dump(file_to_push, jsonfile)
    except:
        raise Exception(f'НЕВЕРНОЕ НАИМЕНОВАНИЕ ФАЙЛА: {json_name}')


def take_from_json(json_name):
    try:
        if os.path.exists(json_name) == False:
            logging.error(f'Файла с названием: ({json_name}) не существует')
        with open(json_name) as jsonfil:
            jsonfile = json.load(jsonfil)
        return jsonfile
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

def from_date_function():
    config_json = take_from_json("config.json")
    date_of_lastrecount = take_from_json(config_json["ltime"])

def get_last_date_time():
    config_json = take_from_json("config.json")
    date_of_lastrecount = take_from_json(config_json["ltime"])
    date = datetime(
        date_of_lastrecount["year"],
        date_of_lastrecount["month"],
        date_of_lastrecount["day"],
        date_of_lastrecount["hour"],
        date_of_lastrecount["minute"],
        date_of_lastrecount["second"]).isoformat() + 'Z'
    return date

def get_now_date():
    date_now = datetime.now()
    datetime(
        date_now.year,
        date_now.month,
        date_now.day,
        date_now.hour,
        date_now.minute,
        date_now.second).isoformat() + 'Z'
    return date_now

def last_date_update(date_now):
    config_json = take_from_json("config.json")
    date_of_lastrecount = take_from_json(config_json["ltime"])
    date_of_lastrecount["year"] = date_now.year
    date_of_lastrecount["month"] = date_now.month
    date_of_lastrecount["day"] = date_now.day
    date_of_lastrecount["hour"] = date_now.hour
    date_of_lastrecount["minute"] = date_now.minute
    date_of_lastrecount["second"] = date_now.second
    push_to_json(config_json["ltime"], date_of_lastrecount)

def get_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    config_json = take_from_json("config.json")
    creds = None
    if os.path.exists(config_json["token"]):
        creds = Credentials.from_authorized_user_file(
            config_json["token"], SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config_json["credentials"], SCOPES)
            creds = flow.run_local_server(
                port=0, access_type='offline', prompt='consent')
        creds_to_json = creds.to_json()
        push_to_json(config_json["token"], creds_to_json, 1)
    service = build('calendar', 'v3', credentials=creds)
    return service

def processing_event(event):
    errors = ''
    config_json = take_from_json("config.json")
    babki_json = take_from_json(config_json["moneycount"])
    event_start = event['start'].get('dateTime', event['start'].get('date'))
    summary = event.get('summary', 'Нет названия')
    description = event.get('description', 'Нет описания')
    if summary == "Нет названия":
        return
    else:
        summary_list = list(summary.split())
        if ("урок" in summary_list) or ("Урок" in summary_list):
            if not description.isnumeric():
                logging.error(
                    f'НЕПРАВИЛЬНЫЙ ФОРМАТ ОПИСАНИЯ!\n {summary};\n Дата занятия: {event_start};\n Описание - {description}')
                errors += f'НЕПРАВИЛЬНЫЙ ФОРМАТ ОПИСАНИЯ!\n {summary};\n Дата занятия: {event_start};\n Описание - {description}\n\n'
                return
            if summary_list[0] not in babki_json:
                babki_json[summary_list[0]] = -int(description)
            else:
                babki_json[summary_list[0]] -= int(description)
        elif ("Группа" in summary_list) or ("группа" in summary_list):
            description_list = list(description.split())
            for i in range(0, len(description_list) - 1, 2):
                if not description_list[i + 1].isnumeric():
                    logging.error(
                        f'НЕПРАВИЛЬНЫЙ ФОРМАТ ОПИСАНИЯ!\n {summary};\n {i};\n Дата занятия: {event_start};\n Описание - {description}\n\n')
                    errors += f'НЕПРАВИЛЬНЫЙ ФОРМАТ ОПИСАНИЯ!\n {summary};\n {i};\n Дата занятия: {event_start};\n Описание - {description}\n\n'
                    continue
                if description_list[i] not in babki_json:
                    babki_json[description_list[i]] = -int(description_list[i + 1])
                else:
                    babki_json[description_list[i]] -= int(description_list[i + 1])
    push_to_json(config_json["moneycount"], babki_json)
    return errors