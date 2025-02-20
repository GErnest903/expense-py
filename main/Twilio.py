from twilio.rest import Client

class TwilHand:
    def __init__(self):
        self.account_sid = 'ACCOUNT'
        self.auth_token = "TOKEN"
        self.client = Client(self.account_sid, self.auth_token)

    def send_events(self, events):
        eventList = ''
        total = 0
        for val in events:
            payTo = val[val.find('-')+1:val.find('$')]
            amount = val[val.find('$')+1: val.find('#')]
            extra = val[val.find('#'):]
            eventList +=(amount + ' to ' + payTo + ' details ' + extra + '\n')
            total += int(amount)
            
        eventList += 'Total Due this week: $' + str(total)
       
        self.client.messages.create(
            body = eventList,
            from_ = "+12183777447",
            to = "+17343651359"
            )
        return eventList
