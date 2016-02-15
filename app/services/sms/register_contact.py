from sms_model import CompanyContacts
import json
from json import JSONEncoder


# - Functions
def store_contact(contact):
    class ContactEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

    json_contact = (ContactEncoder().encode(contact))
    with open("contacts.json", "w") as outfile:
        json.dump(json_contact, outfile)

def register_contact(first_name, last_name, primary_phone):
    contact = CompanyContacts(first_name, last_name, primary_phone)
    store_contact(contact)
    return contact

if __name__ == '__main__':
    # Input
    print("Welcome to contact registration.")
    print("")
    first_name_input = input("Enter first name: ")
    last_name_input = input("Enter last name: ")
    primary_phone_input = input("Enter primary phone #: ")

    # Write
    new_contact = register_contact(first_name_input, last_name_input, primary_phone_input)

    # Confirmation
    print("Thank you for registering, ", new_contact.first_name, ".")
