import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
from datetime import datetime
import os.path

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

with open("config.json") as file:
    config = json.load(file)

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            ccreds = flow.run_local_server(port=0, access_type='offline', prompt='consent')
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    with open('lasttimerecount.json') as timecheck:
        date_of_lastrecount = json.load(timecheck)
    datenow = datetime.now()
    from_date = datetime(date_of_lastrecount["year"], date_of_lastrecount["month"], date_of_lastrecount["day"], date_of_lastrecount["hour"], date_of_lastrecount["minute"], date_of_lastrecount["second"]).isoformat() + 'Z'
    to_date = datetime(datenow.year, datenow.month, datenow.day, datenow.hour, datenow.minute, datenow.second).isoformat() + 'Z'
    date_of_lastrecount["year"] = datenow.year
    date_of_lastrecount["month"] = datenow.month
    date_of_lastrecount["day"] = datenow.day
    date_of_lastrecount["hour"] = datenow.hour
    date_of_lastrecount["minute"] = datenow.minute
    date_of_lastrecount["second"] = datenow.second
    with open('lasttimerecount.json', 'w') as dattt:
        json.dump(date_of_lastrecount, dattt)
#Потом заменишь primary на config[calendarid] который в конфиге вставить надо будет, норм же?
    events_result = service.events().list(calendarId='primary', timeMin=from_date, timeMax=to_date,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('Нет предстоящих событий.')
    with open("babkibabkisukababki.json") as babki:
        babkijson = json.load(babki)
    for event in events:
        summary = event.get('summary', 'Нет названия')
        description = event.get('description', 'Нет описания')
        if summary == "Нет названия":
            continue
        else:
            summary_list = list(summary.split())
            if "Урок" in summary_list:
                if description == 'Нет описания':
                    continue
                if summary not in babkijson:
                    babkijson["Ученики"][summary] = -int(description)
                else:
                    babkijson["Ученики"][summary] -= int(description)
            elif "Группа" in summary_list:
                if description == 'Нет описания':
                    continue
                if summary_list[1] not in babkijson["Группы"]:
                    description_list = list(description.split())
                    babkijson["Группы"][summary_list[1]] = {}
                    for i in range(0, len(description_list) - 1):
                        if i % 2 == 0:
                            babkijson["Группы"][summary_list[1]][description_list[i]] = -int(description_list[i + 1])
                else:
                    description_list = list(description.split())
                    for i in range(0, len(description_list) - 1):
                        if i % 2 == 0:
                            if description_list[i] not in babkijson["Группы"][summary_list[1]]:
                                babkijson["Группы"][summary_list[1]][description_list[i]] = -int(description_list[i + 1])
                            else:
                                babkijson["Группы"][summary_list[1]][description_list[i]] -= int(description_list[i + 1])


    with open("babkibabkisukababki.json", "w") as babochki:
        json.dump(babkijson, babochki)
#    for event in events:
#        start = event['start'].get('dateTime', event['start'].get('date'))
#        summary = event.get('summary', 'Нет названия')
#        description = event.get('description', 'Нет описания')
#        print(f"Начало: {start}, Название: {summary}, Описание: {description}")