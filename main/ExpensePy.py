import datetime
import os.path
import pickle

from est_Credentials import est_Credentials
import CalHandler

from sender import Sender

SCOPESC = ["https://www.googleapis.com/auth/calendar","https://www.googleapis.com/auth/gmail.compose"]

def main():
    print("Setting Credentials")
    credentials = est_Credentials(SCOPESC, "token.json", AUTH_TOKEN)

    #Retrieves paydates, upcoming and next paydate(used as a guide for getting cal events)
    dateData = 0
    print("Setting dates")
    with open('data.pickle', 'rb') as file:
        dateData = pickle.load(file)
        
    #sets dates from file
    payday = dateData[0]
    nextPayday = dateData[1]
    print(payday)

    #today
    today = datetime.datetime.today()
    
    #checks to ensure that today is within 3 days of payday to send message and updates dates
    if (today.date() == payday.date() - datetime.timedelta(days = 3)):
        print("Establishing calendar")
        calHand = CalHandler.CalHandler(credentials)
        print("Establishing Gmail")
        send = Sender(credentials)

        payday = nextPayday
        nextPayday = payday + datetime.timedelta(days = 14)
        newDateData = [payday, nextPayday]
        with open('data.pickle','wb') as file:
            pickle.dump(newDateData, file)
            
        print("Dates Written to file")
        
        headers = calHand.searchExp((payday.isoformat() + "Z"),(nextPayday.isoformat() + "Z"))
        events = send.send_msg( headers, USER_EMAIL, USER_EMAIL)
    else: 
        events = "Not soon enough to pay day Credentials Refreshed" 
        print(events)
    with open('log.txt', 'a') as f:
        f.write('\n')
        f.write(events)
        f.write('\n')
        f.write(today.isoformat())
        f.write(' Success')
        ##DELETE TEST 


if __name__ == "__main__":
  main()

  
