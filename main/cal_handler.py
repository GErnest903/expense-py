import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class cal_handler:
    def __init__(self, creds):
        self.creds = creds
        self.build = build("calendar", "v3", credentials = creds)
        self.now = datetime.datetime.utcnow().isoformat() + "Z"
        self.epEvents = 0
        self.eventHeaders = []

    def searchExp(self, payd, nextPay):
        epEventResults = self.build.events().list(
            calendarId="primary",
            timeMin= payd,
            timeMax=nextPay,
            q = "EP-",
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        self.epEvents = epEventResults.get("items", [])

        for event in self.epEvents:
          self.eventHeaders.append(event["summary"])
        return self.eventHeaders
          
    def create_event(self, values):
        event = {
            'summary': values['summary'],
            'location': values['location'],
            'start': {
                'dateTime': values['start_time'],
                'timeZone': 'America/Detroit'
                },
            'end': {
                'dateTime': values['end_time'],
                'timeZone': 'America/Detroit'
                }
            }
        event = self.build.events().insert(calendarId = 'primary', body = event).execute()
        print('Event made')
        print (event.get('htmlLink'))
                
            
        
    

        
