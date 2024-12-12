import logging
from datetime import datetime
from util import push_to_json, take_from_json, get_last_date_time, get_now_date, last_date_update, get_service, processing_event

def recount():
    config_json = take_from_json("config.json")
    service = get_service()

    date_now = datetime.now()
    from_date = get_last_date_time()
    to_date = get_now_date()
    last_date_update(date_now)

    events_result = service.events().list(
        calendarId=config_json["calendarid"],
        timeMin=from_date,
        timeMax=to_date,
        singleEvents=True,
        orderBy='startTime').execute()

    events = events_result.get('items', [])
    errors = ''
    if not events:
        logging.info('Нет предстоящих событий.\n\n')
    babki_json = take_from_json(config_json["moneycount"])
    for event in events:
        errors += processing_event(event)
    return errors
