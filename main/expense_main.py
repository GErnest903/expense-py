import datetime
import os.path
import pickle
import configparser

from est_Credentials import est_Credentials
import cal_handler

from sender import Sender

SCOPESC = ["https://www.googleapis.com/auth/calendar","https://www.googleapis.com/auth/gmail.compose"]

def main():
    log = open('log.txt', 'a')
    #Reads config file to get main client token path and users email
    print('Reading Config', file = log)
    config = configparser.ConfigParser()
    config.read("config.ini")
    CLIENT_PATH = config.get('GENERAL', 'token_path')
    USER_EMAIL = config.get('GENERAL', 'user_email')
    #tries establishing credentials using information
    print("Setting Credentials", file = log)
    credentials = est_Credentials(SCOPESC, "token.json", CLIENT_PATH)

    #Retrieves paydates, upcoming and next paydate(used as a guide for getting cal events)
    dateData = 0
    payday = 0
    nextPayday = 0
    print("Setting dates", file = log)
    #Checks for pickle data if not reads payday from config file and 
    #establishes pickle data for next use
    try:
        with open('data.pickle', 'rb') as file:
            dateData = pickle.load(file)
        payday = dateData[0]
        nextPayday = dateData[1]
    except FileNotFoundError:
        print('no data.pickle', file = log)
        payday = 1
        print('Reading Config file for date', file = log)
        payday = datetime.datetime.strptime(config.get('GENERAL', 'pay_date'), '%y/%m/%d')
        nextPayday = payday + datetime.timedelta(days = int(config.get('GENERAL', 'days_between_pay')))
        #writes dates to a .pickle
        with open('data.pickle','wb') as file:
            pickle.dump([payday,nextPayday], file)
            print('.pickle Written', file = log)

    #sets dates from file


    #today
    today = datetime.datetime.today()
    
    #checks to ensure that today is within 3 days of payday to send message and updates dates"
    if (today.date() == payday.date() - datetime.timedelta(days = 3)):
        print("Establishing calendar", file = log)
        calHand = cal_handler.CalHandler(credentials)
        print("Establishing Gmail", file = log)
        send = Sender(credentials)

        payday = nextPayday
        nextPayday = payday + datetime.timedelta(days = 14)
        newDateData = [payday, nextPayday]
        with open('data.pickle','wb') as file:
            pickle.dump(newDateData, file)
            
        print("New Dates Written to file", file = log)
        
        headers = calHand.searchExp((payday.isoformat() + "Z"),(nextPayday.isoformat() + "Z"))
        events = send.send_msg( headers, USER_EMAIL, USER_EMAIL)
        with open('log.txt', 'a') as f:
            f.write('\n')
            f.write(events)
            f.write('\n')
            f.write(today.isoformat())
            f.write(' Success')
    else: 
        events = "Not soon enough to pay day Credentials Refreshed" 
        print(events, file = log)
        print(today, file = log)
        print('\n', file = log)

        ##DELETE TEST 


if __name__ == "__main__":
  main()

  
