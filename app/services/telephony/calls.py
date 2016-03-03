# - Notes
# REST API Guide: https://www.twilio.com/docs/api/twiml/sms/twilio_request
# API Root: https://api.twilio.com/2010-04-01/Accounts/ACe0b46c755c8f0b144c1a31e0a9170cea/

# - Imports
import random
import twilio.twiml
from twilio.rest import TwilioRestClient
try:
    from .contacts import CompanyContacts
except:
    from contacts import CompanyContacts

# - Variables
account_sid = "ACe0b46c755c8f0b144c1a31e0a9170cea"
auth_token = "c98aa40b61818e730920459b83ec0f4d"


# - Functions
def manually_call(): # <- Unused
    # client = TwilioRestClient(account_sid, auth_token)
    # to = "+12316851234"
    # from_ = "+10000000000"
    # body = CompanyContacts.check_in(from_)
    # client.messages.create(to, from_, body)
    return ""


def call_response():
    resp = twilio.twiml.Response()

    # Randomly chooses confirmation that is either pre-recording, or text-to-speech.
    confirmation = random.choice(["say", "play"])
    if confirmation == "play":
        resp.play("http://www.sonshinecompanioncare.com/scccheckin01.mp3")
    elif confirmation == "say":
        resp.say("You have successfully checked in. Thank you for using Sunshine Companion Care, and have a wonderful day!", voice="alice")
    else:
        resp.say("You have successfully checked in. Thank you for using Sunshine Companion Care, and have a wonderful day!")

    return str(resp)

# Sub-function of: call_check_in_data
def get_incoming_call_phone_numbers(id=account_sid, pw=auth_token):
    client = TwilioRestClient(id, pw)

    calls = client.calls.list()
    incoming_phone_numbers = []

    for call in calls:
        incoming_phone_numbers.append(call.from_)
    return incoming_phone_numbers

# Sub-function of: call_check_in_data
def get_timestamps(id=account_sid, pw=auth_token):
    client = TwilioRestClient(id, pw)
    calls = client.calls.list()
    timestamps = []

    for call in calls:
        timestamps.append(str(call.date_created))

    return timestamps

# Sub-function of: call_check_in_data
def get_individual(identifier):
    customer_contact = CompanyContacts.get_customer_contact(primary_phone=identifier)
    contact = CompanyContacts.get_contact(primary_phone=identifier)

    if identifier in customer_contact:
        individual = {"first_name": contact[identifier]["first_name"],
                      "last_name": contact[identifier]["last_name"],
                      "primary_phone": identifier}
    elif identifier in contact:
        individual = {"first_name": contact[identifier]["first_name"],
                      "last_name": contact[identifier]["last_name"],
                      "primary_phone": identifier}
    else:
        individual = {"first_name": "Unknown",
                      "last_name": "Unknown",
                      "primary_phone": identifier}

    return individual


def call_check_in_data():
    identifiers = get_incoming_call_phone_numbers()
    timestamps = get_timestamps()
    check_in_data = []
    entry_number = 0
    export = {}

    for identifier in identifiers:
        entry_number += 1
        individual = get_individual(identifier)
        entry = {"id": entry_number, "contact": individual, "phone_number": identifier}
        check_in_data.insert(entry_number - 1, entry)

    entry_number = 0

    for entry in check_in_data:
        entry_number += 1
        id = entry["id"]
        contact = entry["contact"]
        first_name = contact["first_name"]
        last_name = contact["last_name"]
        phone_number = entry["phone_number"]
        timestamp = timestamps[id - 1]

        export[entry_number] = {"timestamp": timestamp, "first_name": first_name, "last_name": last_name, "phone_number": phone_number}

    return export

# !Important! - Turn the following line on when deployed. Turn off for debugging.
# send_message()
if __name__ == "__main__":
    get_individual("lkjkls")
