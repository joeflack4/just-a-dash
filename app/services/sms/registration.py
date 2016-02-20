from contacts import CompanyContacts
import json
from json import JSONEncoder


# - Functions
def store_contact(contact):
    class ContactEncoder(JSONEncoder):
        def default(self, contact):
            return contact.__dict__

    # Open Issue -
    # Multi-line JSON printing - http://stackoverflow.com/questions/2392766/multiline-strings-in-json
    test_dict = {"18509827871":
                 {
                     "first_name": "Joe",
                     "last_name": "Flack"
                 }
             }

    # json_contact = (ContactEncoder().encode(contact))
    # json_contact = (ContactEncoder().encode(test_dict))
    json_contact = test_dict
    with open("contacts.json", "w") as outfile:
        # test = [{"lastname": "lkjskdfj", "name": "ruby"}]
        # print(json_contact)
        # print(type(json_contact))
        formatted_json_contact = json_contact
        for value in json_contact:
            test = 1

        print(formatted_json_contact)
        json.dump(formatted_json_contact, outfile, sort_keys=True, indent=4, separators=(',', ': '))

def register_contact(first_name, last_name, primary_phone):
    contact = CompanyContacts(first_name, last_name, primary_phone)
    print("contact: ", contact.first_name)
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
    # Open Issue -
    # http://stackoverflow.com/questions/15785719/how-to-print-a-dictionary-line-by-line-in-pythonhttp://stackoverflow.com/questions/15785719/how-to-print-a-dictionary-line-by-line-in-python
    print("Thank you for registering, ", new_contact.first_name, ".")
