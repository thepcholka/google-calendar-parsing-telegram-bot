import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging
from datetime import datetime
import os.path
from dfs import push_to_json, take_from_json

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

configjson = take_from_json("config.json")
logging.basicConfig(
    level=logging.INFO,
    filename="lenglogs.txt",
    format="%(asctime)s %(levelname)s %(message)s")


def recount():
    creds = None
    if os.path.exists(configjson["token"]):
        creds = Credentials.from_authorized_user_file(
            configjson["token"], SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                configjson["credentials"], SCOPES)
            creds = flow.run_local_server(
                port=0, access_type='offline', prompt='consent')
        with open(configjson["token"], 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    date_of_lastrecount = take_from_json(configjson["ltime"])

    date_now = datetime.now()
    from_date = datetime(
        date_of_lastrecount["year"],
        date_of_lastrecount["month"],
        date_of_lastrecount["day"],
        date_of_lastrecount["hour"],
        date_of_lastrecount["minute"],
        date_of_lastrecount["second"]).isoformat() + 'Z'
    to_date = datetime(
        date_now.year,
        date_now.month,
        date_now.day,
        date_now.hour,
        date_now.minute,
        date_now.second).isoformat() + 'Z'
    date_of_lastrecount["year"] = date_now.year
    date_of_lastrecount["month"] = date_now.month
    date_of_lastrecount["day"] = date_now.day
    date_of_lastrecount["hour"] = date_now.hour
    date_of_lastrecount["minute"] = date_now.minute
    date_of_lastrecount["second"] = date_now.second
    push_to_json(configjson["ltime"], date_of_lastrecount)
    events_result = service.events().list(
        calendarId=configjson["calendarid"],
        timeMin=from_date,
        timeMax=to_date,
        singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    errors = ''
    if not events:
        logging.info('Нет предстоящих событий.\n\n')
    babki_json = take_from_json(configjson["moneycount"])
    for event in events:
        eventstart = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'Нет названия')
        description = event.get('description', 'Нет описания')
        if summary == "Нет названия":
            continue
        else:
            summary_list = list(summary.split())
            if ("урок" in summary_list) or ("Урок" in summary_list):
                if not description.isnumeric():
                    logging.error(
                        f'НЕПРАВИЛЬНЫЙ ФОРМАТ ОПИСАНИЯ!\n {summary};\n Дата занятия: {eventstart};\n Описание - {description}')
                    errors += f'НЕПРАВИЛЬНЫЙ ФОРМАТ ОПИСАНИЯ!\n {summary};\n Дата занятия: {eventstart};\n Описание - {description}\n\n'
                    continue
                if summary_list[1] not in babki_json:
                    babki_json[summary_list[1]] = -int(description)
                else:
                    babki_json[summary_list[1]] -= int(description)
            elif ("Группа" in summary_list) or ("группа" in summary_list):
                description_list = list(description.split())
                for i in range(0, len(description_list) - 1, 2):
                    if not description_list[i + 1].isnumeric():
                        logging.error(
                            f'НЕПРАВИЛЬНЫЙ ФОРМАТ ОПИСАНИЯ!\n {summary};\n {i};\n Дата занятия: {eventstart};\n Описание - {description}\n\n')
                        errors += f'НЕПРАВИЛЬНЫЙ ФОРМАТ ОПИСАНИЯ!\n {summary};\n {i};\n Дата занятия: {eventstart};\n Описание - {description}\n\n'
                        continue
                    if description_list[i] not in babki_json:
                        babki_json[description_list[i]] = -int(description_list[i + 1])
                    else:
                        babki_json[description_list[i]] -= int(description_list[i + 1])
        push_to_json(configjson["moneycount"], babki_json)
    return errors
