##TODO
##Create Twilio text handler
##Pass the summary string to it
##let twilio handler break down data and prep it for sending message/sending the message

import datetime
import os.path
import pickle

from twilio.rest import Client

from est_Credentials import est_Credentials
import CalHandler
import Twilio

SCOPESC = ["https://www.googleapis.com/auth/calendar"]

def main():
    print("Setting Credentials")
    credentials = est_Credentials(SCOPESC, "calToken.json", "C:/Users/Gabriel/OneDrive/Documents/ExPy/tCredential.json")
    print("Establishing calendar")
    calHand = CalHandler.CalHandler(credentials)
    print("Establishing Twilio")
    twilHand = Twilio.TwilHand()

    #Retrieves paydates, upcoming and next paydate(used as a guide for getting cal events)
    dateData = 0
    with open('data.pickle', 'rb') as file:
        dateData = pickle.load(file)
    #sets dates from file
    payday = dateData[0]
    nextPayday = dateData[1]

    #today
    today = datetime.datetime.today()
    #checks to ensure that today is within 3 days of payday to send message and updates dates
    if (today >= (payday - datetime.timedelta(days = 3))):

        payday = nextPayday
        nextPayday = payday + datetime.timedelta(days = 14)
        newDateData = [payday, nextPayday]
        with open('data.pickle','wb') as file:
            pickle.dump(newDateData, file)
        print("Dates Written to file")

    #This is going to need next next payday, so have upcoming payday and nextpayday
    headers = calHand.searchExp((payday.isoformat() + "Z"),(nextPayday.isoformat() + "Z"))
    events = twilHand.send_events(headers)
    
    with open('log.txt', 'a') as f:
        f.write('\n')
        f.write(events)
        f.write(today.isoformat())
        f.write(' Success')


if __name__ == "__main__":
  main()
