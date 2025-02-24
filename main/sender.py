import os.path

import base64
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Sender:
    def  __init__(self, creds):
        self.service = build("gmail", "v1", credentials = creds)

    def send_msg(self, items, to, fromEmail):
        try:
            eventList = ''
            total = 0
            for val in items:
                date = val[0]
                summ = val[1]
                
                payTo = summ[summ.find('-')+1:summ.find('$')]
                amount = summ[summ.find('$')+1: summ.find('#')]
                extra = summ[summ.find('#'):]
                eventList +=(date + ' $' + amount + ' to ' + payTo + ' details ' + extra + '\n')
                total += int(amount)
            
            eventList += 'Total Due this week: $' + str(total)
            msg = EmailMessage()
            msg.set_content(eventList)
            msg["To"] = to
            msg["From"] = fromEmail
            msg["Subject"] = "AUTO EXPENSE REPORT"

            encoded_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
            create_message = {"raw": encoded_message}
            send_message = (
                    self.service.users()
                    .messages()
                    .send(userId= "me", body=create_message)
                    .execute()
                    )
            print(f'Message ID: {send_message["id"]}')
        except HttpError as error:
            print(error)
        
        return eventList

