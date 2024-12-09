import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
import logging
from datetime import datetime
import os.path
from defs import pushtojson, takefromjson
from botfunctions import senderror

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

configjson = takefromjson("config.json")
logging.basicConfig(level=logging.INFO, filename="lenglogs", format="%(asctime)s %(levelname)s %(message)s")

def recount():
    creds = None
    if os.path.exists(configjson["token"]):
        creds = Credentials.from_authorized_user_file(configjson["token"], SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(configjson["credentials"], SCOPES)
            ccreds = flow.run_local_server(port=0, access_type='offline', prompt='consent')
        with open(configjson["token"], 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    date_of_lastrecount = takefromjson(configjson["ltime"])

    datenow = datetime.now()
    from_date = datetime(date_of_lastrecount["year"], date_of_lastrecount["month"], date_of_lastrecount["day"], date_of_lastrecount["hour"], date_of_lastrecount["minute"], date_of_lastrecount["second"]).isoformat() + 'Z'
    to_date = datetime(datenow.year, datenow.month, datenow.day, datenow.hour, datenow.minute, datenow.second).isoformat() + 'Z'
    date_of_lastrecount["year"] = datenow.year
    date_of_lastrecount["month"] = datenow.month
    date_of_lastrecount["day"] = datenow.day
    date_of_lastrecount["hour"] = datenow.hour
    date_of_lastrecount["minute"] = datenow.minute
    date_of_lastrecount["second"] = datenow.second

    pushtojson(date_of_lastrecount, configjson["ltime"])
#Потом заменишь primary на config[calendarid] который в конфиге вставить надо будет, норм же?
    events_result = service.events().list(calendarId='primary', timeMin=from_date, timeMax=to_date,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('Нет предстоящих событий.')
        babkijson = takefromjson(configjson["moneycount"])
    for event in events:
        eventstart = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'Нет названия')
        description = event.get('description', 'Нет описания')
        if summary == "Нет названия":
            continue
        else:
            summary_list = list(summary)
            if "урок" or "Урок" in summary_list:
                if not description.isnumeric():
                    logging.error(f'НЕПРАВИЛЬНЫЙ ФОРМАТ ОПИСАНИЯ! {summary}; Дата занятия: {eventstart}; Описание - {description}')
                    senderror(f'НЕПРАВИЛЬНЫЙ ФОРМАТ ОПИСАНИЯ! {summary}; Дата занятия: {eventstart}; Описание - {description}')
                    continue
                if summary not in babkijson:
                    babkijson[summary] = -int(description)
                else:
                    babkijson[summary] -= int(description)
            elif "Группа" or "группа" in babkijson:
                description_list = list(description)
                for i in range(1, len(description_list) - 1):
                    if not description_list[i + 1].isnumeric():
                        logging.error(f'НЕПРАВИЛЬНЫЙ ФОРМАТ ОПИСАНИЯ! {summary}; {i}; Дата занятия: {eventstart}; Описание - {description}')
                        senderror(f'НЕПРАВИЛЬНЫЙ ФОРМАТ ОПИСАНИЯ! {summary}; {i}; Дата занятия: {eventstart}; Описание - {description}')
                        continue
                    if i % 2 == 0:
                        if description_list[i] not in babkijson:
                            babkijson[description_list[i]] = -int(description_list[i + 1])
                        else:
                            babkijson[description_list[i]] -= int(description_list[i + 1])
    pushtojson(babkijson, configjson["moneycount"])