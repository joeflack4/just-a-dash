# - Notes
# * Setting up a class -
#   https://www.jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/
# * Optional class arguments - http://stackoverflow.com/questions/4841782/python-constructor-and-default-value
import json


# - Classes
class CompanyContacts:
    def __init__(self, first_name, last_name, primary_phone, contact_type=None,
                 secondary_phone_01=None, secondary_phone_02=None, secondary_phone_03=None):
        self.first_name = first_name
        self.last_name = last_name
        self.primary_phone = primary_phone
        if contact_type is None:
            self.contact_type = ""
        else:
            self.contact_type = contact_type
        if secondary_phone_01 is None:
            self.secondary_phone_01 = ""
        else:
            self.secondary_phone_01 = secondary_phone_01
        if secondary_phone_02 is None:
            self.secondary_phone_02 = ""
        else:
            self.secondary_phone_02 = secondary_phone_02
        if secondary_phone_03 is None:
            self.secondary_phone_03 = ""
        else:
            self.secondary_phone_03 = secondary_phone_03

    # Open Issue
    # http://stackoverflow.com/questions/16129652/accessing-json-elements
    def test(self):
        return "test"

    def get_contact(self, primary_phone):
        with open("contacts.json", "r") as contacts_file:
            contacts = json.loads(contacts_file.read())
            contact = contacts
            return contact

    def check_in(self):
        return "Thanks, ", self.first_name, ". You have successfully checked in."
