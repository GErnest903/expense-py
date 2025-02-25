"""


"""
import datetime
import os.path
import pickle
import configparser

from est_credentials import est_credentials
from cal_reader import cal_reader

from sender import sender

SCOPESC = ["https://www.googleapis.com/auth/calendar","https://www.googleapis.com/auth/gmail.compose"]

def main():
    #Creates log file
    log = open('log.txt', 'a')
    #Reads config file to get main client token path and users email
    print("Reading Config" + str(datetime.datetime.now()))
    config = configparser.ConfigParser()
    config.read('config.ini')
    CLIENT_PATH = config.get('GENERAL', 'token_path')
    USER_EMAIL = config.get('GENERAL', 'user_email')
    #tries establishing credentials using information
    print("Setting Credentials" + str(datetime.datetime.now()))
    credentials = est_credentials(SCOPESC, 'token.json', CLIENT_PATH)

    #Retrieves paydates, upcoming and next paydate(used as a guide for getting cal events)
    dateData = 0
    payday = 0
    days_between = 0
    nextPayday = 0
    print("Setting dates" + str(datetime.datetime.now()))
    #Checks for pickle data if not reads payday from config file and 
    #establishes pickle data for next use
    try:
        with open('data.pickle', 'rb') as file:
            dateData = pickle.load(file)

        payday = dateData[0]
        nextPayday = dateData[1]
        days_between = dateData[2]
    except FileNotFoundError:
        print("no data.pickle " + str(datetime.datetime.now()))
        print("Reading Config file for dates " + str(datetime.datetime.now()))

        payday = datetime.datetime.strptime(config.get('GENERAL', 'pay_date'), '%y/%m/%d')
        days_between = int(config.get('GENERAL', 'days_between_pay'))
        nextPayday = payday + datetime.timedelta(days = days_between )

        #writes dates to a .pickle
        with open('data.pickle','wb') as file:
            pickle.dump([payday,nextPayday, days_between], file)
            print(".pickle Written " + str(datetime.datetime.now()), file = log)

    today = datetime.datetime.today()

    #checks to ensure that today is within 3 days of payday to send message and updates dates"
    if (today.date() == payday.date() - datetime.timedelta(days = 3)):
	#builds calendar instance
        print("Establishing calendar " + str(datetime.datetime.now()))
        calHand = cal_reader(credentials)

	#builds gmail instance
        print("Establishing Gmail " + str(datetime.datetime.now()))
        send = sender(credentials)
	#uses cal api to gather titles and dates for expense due dates
        print("Gathering events " + str(datetime.datetime.now()))
        headers = calHand.searchExp((payday.isoformat() + "Z"),(nextPayday.isoformat() + "Z"))
	#passes headers to sender to format and send msg
        events = send.send_msg( headers, USER_EMAIL)

	#sets next set of paydays
        payday = nextPayday
        nextPayday = payday + datetime.timedelta(days = days_between)
        newDateData = [payday, nextPayday, days_between]
        with open('data.pickle','wb') as file:
            pickle.dump(newDateData, file)

        print("New Dates Written to file " + str(datetime.datetime.now()), file = log)

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


if __name__ == "__main__":
  main()
