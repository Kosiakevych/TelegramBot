from google.oauth2 import service_account
from googleapiclient.discovery import build

from days import current_date


class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    FILE_PATH = 'xandr-1-cf9958cace58.json'

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            filename=self.FILE_PATH, scopes=self.SCOPES
        )
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def add_calendar(self, calendar_id):
        calendar_list_entry = {
            'id': calendar_id
        }
        return self.service.calendarList().insert(body=calendar_list_entry).execute()

    def add_event(self, calendar_id, body):
        return self.service.events().insert(calendarId=calendar_id, body=body).execute()


obj = GoogleCalendar()
name_calendar_id = 'sashacaha2019@gmail.com'


# create event in google calendar
def total(client_name: list, client_description: list, client_date: list, client_time: list):
    # ['2023', '01', '26'] ['15'] - > '2023-01-26T15:00:00' | for google calendar API
    date_cal = f'{"-".join(client_date)}T{client_time[0]}:00:00'

    # Add event
    event = {
        'summary': ', '.join(client_name),  # ['Alex', '123'] -> 'Alex, 123'
        # ['Депиляция', 'Бикини'], current_date() -> Депиляция, Бикини, 2023_01_12
        'description': f"{''.join(client_description)}\n\n📥 Запись создана: {current_date()}",
        'start': {
            'dateTime': date_cal,  # '2023-01-26T15:00:00'
            'timeZone': 'Europe/Berlin',
        },
        'end': {
            'dateTime': date_cal.replace(':00', ':40'),  # '2023-01-26T15:00:00' ->  '2023-01-26T15:40:00'
            'timeZone': 'Europe/Berlin',
        },
    }
    obj.add_event(calendar_id=name_calendar_id, body=event)  # add event into google calendar


# get entry of client
def get_calendar_data(name: str):
    take_events = obj.service.events().list(calendarId=name_calendar_id).execute()  # get data from all event
    info = []  # create to collect info from user entry
    title = []  # create for text of button
    event_id = []  # collect eventID for (delete_event)
    how_many = range(len(take_events['items']))  # how many entry has user
    for i in how_many:
        if take_events['items'][i]['summary'] == name:  # if name of user in calendar event

            # for my_entry:delete
            date = f"{take_events['items'][i]['start']['dateTime'][:10]}"  # 2022-12-11
            time = f" {take_events['items'][i]['start']['dateTime'][11:13]}:00"  # 14:00
            title.append(['Удалить запись: ', date, time])  # [Удалить запись: , '2022-12-11', '14:00']
            event_id.append(take_events['items'][i]['id'])  # append eventID

            # for my_entry:my
            info.append(f"<b>Дата</b> : <u>{date}</u>\n"
                        f"<b>Время</b> : <u>{time}</u>\n"
                        f"<b>Услуга</b> :\n🤍 <b>{take_events['items'][i]['description']}</b>\n"
                        f"----------------------------------------\n")

    return how_many, info, title, event_id


def delete_event(event_id: str):  # delete event
    obj.service.events().delete(calendarId=name_calendar_id, eventId=event_id).execute()


def my_entry_list(client_name: list) -> str and list:
    get_data = get_calendar_data(', '.join(client_name))  # ['Alex', '123'] -> 'Alex, 123'
    text = '<b>📘Ваши записи:</b>\n\n'  # text for message.edit_text
    for i in range(len(get_data[1])):  # for all data what we have
        text += get_data[1][i]  # Ваши записи:| (Дата : 2022-12-19 | Время : 15:00) * what we have
    return text, get_data[2]


def check_free_space(date: str) -> bool:  # if date that user chose was free -> True
    all_event = obj.service.events().list(calendarId=name_calendar_id).execute()  # get data from all event
    all_date = []  # date that user can not make an entry
    for events in all_event['items']:
        all_date.append(events["start"]["dateTime"].split(":")[0])  # 2022-01-31T16:00:00+01:00' -> 2022-01-31T16
    if not date in all_date:
        return True
    return False
