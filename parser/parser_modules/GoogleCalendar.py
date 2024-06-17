import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import groups, eng_groups

logging.basicConfig(filename="logs/calendar_logs.log", level=logging.INFO,
                    format=' %(asctime)s - %(levelname)s - %(message)s',
                    encoding="utf8")

SCOPES = ['https://www.googleapis.com/auth/calendar']

SERVICE_ACCOUNT_FILE = 'credentials.json'


class GoogleCalendar(object):
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = build('calendar', 'v3', credentials=credentials, cache_discovery=False)

    def create_event(self, event, calendarID):
        del event['group']
        ex = self.service.events().insert(calendarId=calendarID,
                                          body=event).execute()

        logging.info(f"event created {event['summary']}")

    def delete_id(self, event_id, calendarID):
        self.service.events().delete(calendarId=calendarID, eventId=event_id).execute()
        logging.info(f"event deleted id {event_id}")

    def get_list(self, calendarID):
        ex = self.service.events().list(calendarId=calendarID, maxResults=9999).execute()
        items = ex.get("items")
        return items

    def get_list_dict(self, calendarID):
        prev_timetable = []
        events = self.get_list(calendarID)

        group = ''

        for gr in groups:
            if calendarID in gr['ids']:
                index = gr['ids'].index(calendarID)
                group = gr['subgroups'][index]
                break

        if group == '':
            for gr in eng_groups:
                if eng_groups[gr]['id'] == calendarID:
                    group = gr
                    break

        for e in events:
            event_dict = {
                'summary': e.get('summary'),
                'description': e.get('description'),
                'location': e.get('location'),
                'start': e.get('start'),
                'end': e.get('end'),
                'group': group,
                'id': e.get('id')
            }

            if event_dict['description'] is None:
                event_dict['description'] = ''

            if event_dict['location'] is None:
                event_dict['location'] = ''

            prev_timetable.append(event_dict)
        return prev_timetable
