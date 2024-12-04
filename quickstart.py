from datetime import datetime
import os.path
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Если измените эти области, удалите файл token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    time_min = datetime(2023, 1, 1, 0, 0, 0).isoformat() + 'Z'  # 'Z' означает UTC время
    time_max = datetime(2024, 12, 31, 23, 59, 59).isoformat() + 'Z'  # 'Z' означает UTC время

    events_result = service.events().list(calendarId='primary', timeMin=time_min, timeMax=time_max,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('Нет предстоящих событий.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'Нет названия')
        description = event.get('description', 'Нет описания')
        print(f"Начало: {start}, Название: {summary}, Описание: {description}")

if __name__ == '__main__':
    main()