# - Notes
# Download the twilio-python library from http://twilio.com/docs/libraries
import twilio.twiml
from twilio.rest import TwilioRestClient
try:
    from .contacts import CompanyContacts
except:
    from contacts import CompanyContacts

# - Functions
# Find these values at https://twilio.com/user/account
account_sid = "MG57a8a1ed371abc4940a03ce17c61f07b"
auth_token = "YYYYYYYYYYYYYYYYYY"

def sms_response():
    resp = twilio.twiml.Response()
    # To Do: Replace 'from' later on when using the Twilio API.
    from_ = "+10000000000"
    body = CompanyContacts.check_in(from_)
    resp.message(body)
    return str(resp)

def send_message():
    client = TwilioRestClient(account_sid, auth_token)
    to = "+12316851234"
    # To Do: Replace 'from' later on when using the Twilio API.
    from_ = "+10000000000"
    body = CompanyContacts.check_in(from_)
    # message = client.messages.create(to, from_, body)
    client.messages.create(to, from_, body)

# !Important! - Turn the following line on when deployed. Turn off for debugging.
# send_message()

if __name__ == "__main__":
    # fake_user_input = "+18509827871"
    # CompanyContacts.contacts(fake_user_input)
    sms_response()
