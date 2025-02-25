import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class cal_reader:
    def __init__(self, creds):
        self.creds = creds
        self.build = build("calendar", "v3", credentials = creds)
        self.eventHeaders = []

    def searchExp(self, payd, nextPay):
	#Searches for any calendar events that start with EP- and stores them in a list paired with their date
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
            self.eventHeaders.append([event['start'].get('dateTime', event['start'].get('date')), event["summary"]])

        return self.eventHeaders
