from __future__ import print_function
from datetime import datetime, timedelta, timezone
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from gcal_conky.helper import get_absolute_path, replace_text_in_file
from gcal_conky.configuration import Configuration
from gcal_conky.event import Event

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


# Use the json file instead
def get_creds(config: Configuration):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    pickle_path = get_absolute_path(config.get("pickle_path"))
    credentials_path = get_absolute_path(config.get("credentials_path"))

    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pickle_path, 'wb') as token:
            pickle.dump(creds, token)
    return creds


def get_start_of_day(config: Configuration):
    # return only events that start before midnight
    start = datetime.utcnow()
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    start = start + timedelta(hours=config.get('utc_offset'))
    start = start.isoformat() + "Z"
    return start


def get_end_of_day(config: Configuration):
    # return only events that start before midnight
    end = datetime.utcnow() + timedelta(days=1)
    end = end.replace(hour=0, minute=0, second=0, microsecond=0)
    end = end + timedelta(hours=config.get('utc_offset'))
    end = end.isoformat() + "Z"
    return end


def fetch_todays_events():

    config = Configuration()
    creds = get_creds(config)
    output_path = get_absolute_path(config.get('today')['output_path'])

    service = build('calendar', 'v3', credentials=creds)

    # start = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    start = get_start_of_day(config)
    end = get_end_of_day(config)

    events = []
    for calendar in config.get('calendars'):
        events_result = service.events().list(calendarId=calendar,
                                              timeMin=start,
                                              timeMax=end,
                                              singleEvents=True,
                                              orderBy='startTime'
                                              ).execute()
        for event in events_result.get('items', []):
            event_start = event['start'].get('dateTime', event['start'].get('date'))
            event_start = datetime.fromisoformat(event_start)
            if event_start.tzinfo is None:
                event_start = event_start.replace(tzinfo=timezone(timedelta(hours=config.get('utc_offset'))))
            event_end = event['end'].get('dateTime', event['end'].get('date'))
            event_end = datetime.fromisoformat(event_end)
            if event_end.tzinfo is None:
                event_end = event_end.replace(tzinfo=timezone(timedelta(hours=config.get('utc_offset'))))
            events.append(Event(event['summary'], event_start, event_end))

    if not events:
        replace_text_in_file(output_path, config.get('today')['start_tag'], config.get('today')['end_tag'], 'No upcoming events')
        exit(1)

    # print('\n'.join(map(str, events)))
    events = sorted(events)

    output_string = ""
    for event in events:
        now = datetime.now(event.start.tzinfo)  # set now every time, since theoretically the timezone could differ from event to event.
        if event.start < now < event.end:
            output_string += replace_event_in_string(config.get('today')['event_format_now'], event, config)
        elif event.end < now:
            output_string += replace_event_in_string(config.get('today')['event_format_before'], event, config)
        elif now < event.start:
            output_string += replace_event_in_string(config.get('today')['event_format_after'], event, config)
        else:  # shouldn't happen
            output_string += replace_event_in_string(config.get('today')['event_format'], event, config)

    replace_text_in_file(output_path, config.get('today')['start_tag'], config.get('today')['end_tag'], output_string)


def replace_event_in_string(source_string: str, event: Event, config: Configuration):
    return source_string.replace('{event_name}', event.name) \
                        .replace('{event_start}', event.start.strftime(config.get('today')['datetime_format'])) \
                        .replace('{event_end}', event.end.strftime(config.get('today')['datetime_format']))


if __name__ == '__main__':
    fetch_todays_events()
