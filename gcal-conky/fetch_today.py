from __future__ import print_function
from datetime import datetime, timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from helper import print_to_file, get_absolute_path

from configuration import Configuration

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


def get_end_of_day(config: Configuration):
    # return only events that start before midnight
    end = datetime.utcnow() + timedelta(days=1)
    end = end.replace(hour=0, minute=0, second=0, microsecond=0)
    end = end + timedelta(hours=config.get('utc_offset'))
    end = end.isoformat() + "Z"
    return end


def main():

    config = Configuration()
    creds = get_creds(config)
    output_path = get_absolute_path(config.get('output_path'))
    print("output_path ", output_path)

    service = build('calendar', 'v3', credentials=creds)

    start = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    end = get_end_of_day(config)

    events = []
    for calendar in config.get('calendars'):
        events_result = service.events().list(calendarId=calendar,
                                              timeMin=start,
                                              timeMax=end,
                                              singleEvents=True,
                                              orderBy='startTime'
                                              ).execute()
        events.extend(events_result.get('items', []))

    if not events:
        print('No upcoming events found.')
        exit(1)
    else:
        events = sorted(events, key=lambda e: e['start'].get('dateTime', e['start'].get('date')))

    lines = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = datetime.fromisoformat(start)
        start = start.strftime("%H:%M")
        line = "{} - {}".format(start, event['summary'])
        lines.append(line)
    print_to_file(output_path, lines)


if __name__ == '__main__':
    main()
