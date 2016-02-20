# - Notes
# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
from contacts import CompanyContacts


# - Functions
# Find these values at https://twilio.com/user/account
account_sid = "MG57a8a1ed371abc4940a03ce17c61f07b"
auth_token = "YYYYYYYYYYYYYYYYYY"

def send_message():
    client = TwilioRestClient(account_sid, auth_token)
    to = "+12316851234"
    from_ = "+18509827871"
    body = CompanyContacts.contacts(from_)
    # message = client.messages.create(to, from_, body)
    client.messages.create(to, from_, body)

# !Important! - Turn the following line on when deployed. Turn off for debugging.
# send_message()

if __name__ == "__main__":
    fake_user_input = "+18509827871"
    CompanyContacts.contacts(fake_user_input)
