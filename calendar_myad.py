import json
from datetime import datetime
import os.path
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Если измените эти области, удалите файл token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main1():
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
        datettime = json.load(timecheck)
    datenow = datetime.now()
    time_min = datetime(datettime["year"], datettime["month"], datettime["day"], datettime["hour"], datettime["minute"], datettime["second"]).isoformat() + 'Z'  # 'Z' означает UTC время
    time_max = datetime(datenow.year, datenow.month, datenow.day, datenow.hour, datenow.minute, datenow.second).isoformat() + 'Z'  # 'Z' означает UTC время
    datettime["year"] = datenow.year
    datettime["month"] = datenow.month
    datettime["day"] = datenow.day
    datettime["hour"] = datenow.hour
    datettime["minute"] = datenow.minute
    datettime["second"] = datenow.second
    with open('lasttimerecount.json', 'w') as dattt:
        json.dump(datettime, dattt)
    events_result = service.events().list(calendarId='primary', timeMin=time_min, timeMax=time_max,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('Нет предстоящих событий.')
    with open("babkibabkisukababki.json") as babki:
        babk = json.load(babki)
    for event in events:
        summary = event.get('summary', 'Нет названия')
        description = event.get('description', 'Нет описания')
        if description == 'Нет описания':
            continue
        if summary not in babk:
            babk[summary] = -int(description)
        else:
            # !!!!!!!!!!!!!!!!!!!!
            babk[summary] = babk[summary] - int(description)
            # !!!!!!!!!!!!!!!!!!!!
    with open("babkibabkisukababki.json", "w") as babochki:
        json.dump(babk, babochki)
#    for event in events:
#        start = event['start'].get('dateTime', event['start'].get('date'))
#        summary = event.get('summary', 'Нет названия')
#        description = event.get('description', 'Нет описания')
#        print(f"Начало: {start}, Название: {summary}, Описание: {description}")