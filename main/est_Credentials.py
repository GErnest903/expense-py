import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def est_Credentials(SCOPES, token_json, cred_json_path) :
    scopes = SCOPES
    tokeJ = token_json
    credPath = cred_json_path
    creds = None
    #Checks if there is a auth Token already
    if os.path.exists(tokeJ):
        creds = Credentials.from_authorized_user_file(tokeJ, scopes)
    #if not makes one by having user sign in and mark permissions
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("creds refreshed")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credPath, scopes
            )
            creds = flow.run_local_server(port = 0)
            #saves permissions as new token
            with open(tokeJ, "w") as token:
                token.write(creds.to_json())
    return creds
