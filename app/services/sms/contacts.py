# - Notes
# * Setting up a class -
#   https://www.jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/
# * Optional class arguments - http://stackoverflow.com/questions/4841782/python-constructor-and-default-value
import os
import json

# - Setting Boilerplate
# Relative Pathing
__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

# - Classes
class CompanyContacts:
    # - Initialize
    def __init__(self, first_name=None, last_name=None, primary_phone=None , contact_type=None,
                 secondary_phone_01=None, secondary_phone_02=None, secondary_phone_03=None):
        if first_name is None:
            self.first_name = ""
        else:
            self.first_name = first_name
        if last_name is None:
            self.last_name = ""
        else:
            self.last_name = last_name
        if primary_phone is None:
            self.primary_phone = ""
        else:
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
        id = primary_phone

    # - Properties
    # http://stackoverflow.com/questions/17330160/how-does-the-property-decorator-work
    # https://docs.python.org/2/howto/descriptor.html
    @property
    def contact(self):
        @property
        def first_name(self):
            return self
        @property
        def last_name(self):
            return self
        @property
        def contact_type(self):
            return self
        @property
        def primary_phone(self):
            return self
        @property
        def secondary_phone_01(self):
            return self
        @property
        def secondary_phone_02(self):
            return self
        @property
        def secondary_phone_03(self):
            return self
        return self

    # - Variables
    contacts_file = open(os.path.join(__location__, "contacts.json"), "r")
    contacts = json.load(contacts_file)

    # - Static Methods
    @staticmethod
    def static_check_in():
        # return "Thanks, ", contact.first_name, ". You have successfully checked in."
        return "You have successfully checked in. Thank you!"

    # - Methods
    def get_contact(primary_phone):
        with open(os.path.join(__location__, "contacts.json"), "r") as contacts_file:
            contacts = json.loads(contacts_file.read())
            contact = contacts
            return contact

    def contacts_other_functions(*args):

        contacts_file = open(os.path.join(__location__, "contacts.json"), "r")
        # contacts_file = open("contacts.json", "r")
        contacts = json.load(contacts_file)

        def iterator():
            for x in contacts:
                print(x)
                for y in x:
                    print(y)

        def contact_lookup():
            for contact_number in args:
                print("Contact Lookup")
                print("Your Phone #: ", contact_number)
                print("First Name: ", contacts[contact_number]["first_name"])
                print("Last Name: ", contacts[contact_number]["last_name"])

        if "iterate" in args:
            return iterator()
        elif "all" in args:
            return contacts
        else:
            response = contact_lookup()
            return response

    def check_in(*args, contacts=contacts):
        for contact_number in args:
            first_name = str(contacts[contact_number]["first_name"])
            last_name = str(contacts[contact_number]["last_name"])
            return "You have successfully checked in, " + first_name + " " + last_name + "!"


# - Run
if __name__ == "__main__":
    print("")
    fake_user_input = "+18509827871"
    CompanyContacts.contacts(fake_user_input)
