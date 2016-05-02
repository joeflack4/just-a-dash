# - Notes
# REST API Guide: https://www.twilio.com/docs/api/twiml/sms/twilio_request
# API Root: https://api.twilio.com/2010-04-01/Accounts/ACe0b46c755c8f0b144c1a31e0a9170cea/

# - Imports
import random
import twilio.twiml
from twilio.rest import TwilioRestClient
from app.models import OMS_Config, Customers, Personnel
# from app.models import Contacts
try:
    from .contacts import CompanyContacts
except:
    from contacts import CompanyContacts

# - Variables
account_sid = OMS_Config.query.filter_by(key='Twilio Account SID').first().value
auth_token = OMS_Config.query.filter_by(key='Twilio Auth Token').first().value
twilio_number = '+' + OMS_Config.query.filter_by(key='Twilio Phone Number').first().value


# - Functions
def manually_call():  # <- Unused
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
    individual = {}
    phone_identifier = str(identifier)[1:]

    customer_contact = Customers.query.filter_by(phone1=phone_identifier).first()
    customer_contact_secondary_number = Customers.query.filter_by(phone2=phone_identifier).first()
    personnel_contact = Personnel.query.filter_by(phone1=phone_identifier).first()
    personnel_contact_secondary_number = Personnel.query.filter_by(phone1=phone_identifier).first()
    other_contact = Personnel.query.filter_by(phone1=phone_identifier).first()
    other_contact_secondary_number = Personnel.query.filter_by(phone2=phone_identifier).first()

    contact_lookup_methods = (customer_contact, customer_contact_secondary_number, personnel_contact,
                              personnel_contact_secondary_number, other_contact, other_contact_secondary_number)

    try:
        for method in contact_lookup_methods:
            try:
                if type(method) != None:
                    individual = {"first_name": method.name_first,
                                  "last_name": method.name_last,
                                  "primary_phone": method.phone1}
                    break
                else:
                    continue
            except:
                continue
    except:
        individual = {"first_name": "Unknown",
                      "last_name": "Unknown",
                      "primary_phone": identifier}

    if individual == {}:
        individual = {"first_name": "Unknown",
                      "last_name": "Unknown",
                      "primary_phone": identifier}

    return individual


def call_check_in_data():
    identifiers = get_incoming_call_phone_numbers()
    timestamps = get_timestamps()
    check_in_data = []
    export = {}
    i = 0
    list_id = 0

    for identifier in identifiers:
        i += 1
        individual = get_individual(identifier)
        entry = {"id": i, "contact": individual, "phone_number": identifier}
        check_in_data.insert(i - 1, entry)

    for entry in check_in_data:
        list_id += 1
        id = entry["id"]
        contact = entry["contact"]
        first_name = contact["first_name"]
        last_name = contact["last_name"]
        phone_number = entry["phone_number"]
        timestamp = timestamps[id - 1]

        export[list_id] = {"timestamp": timestamp, "first_name": first_name, "last_name": last_name, "phone_number": phone_number}

    return export

# !Important! - Turn the following line on when deployed. Turn off for debugging.
# send_message()
if __name__ == "__main__":
    get_individual("lkjkls")
