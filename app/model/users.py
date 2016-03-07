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
class Users:
    # - Initialize
    def __init__(self, first_name=None, last_name=None, primary_phone=None , user_type=None,
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
        if user_type is None:
            self.user_type = ""
        else:
            self.user_type = user_type
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
    def user(self):
        @property
        def first_name(self):
            return self
        @property
        def last_name(self):
            return self
        @property
        def user_type(self):
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
    users_file = open(os.path.join(__location__, "users.json"), "r")
    users = json.load(users_file)

    # - Static Methods
    @staticmethod
    def static_check_in():
        # return "Thanks, ", user.first_name, ". You have successfully checked in."
        return "You have successfully checked in. Thank you!"

    @staticmethod
    def get_user():
        with open(os.path.join(__location__, "users.json"), "r") as user_file:
            raw_users = json.loads(user_file.read())

            # - Work in progress
            # users = []
            # for user in raw_users:
                # Debugging
                # user_list = []
                # for item in user:
                #     user_list.append(item)
                # users.append(user_list)

                # users.append(user)

            # Debugging
            # print(users)

            return raw_users

    @staticmethod
    def get_users():
        with open(os.path.join(__location__, "users.json"), "r") as user_file:
            raw_users = json.loads(user_file.read())
            return raw_users

    # - Methods
    def get_user(primary_phone):
        with open(os.path.join(__location__, "users.json"), "r") as users_file:
            users = json.loads(users_file.read())
            user = users
            return user

    def get_customer_user(primary_phone):
        with open(os.path.join(__location__, "customer_users.json"), "r") as users_file:
            users = json.loads(users_file.read())
            user = users
            return user

    def users_other_functions(*args):

        users_file = open(os.path.join(__location__, "users.json"), "r")
        # users_file = open("users.json", "r")
        users = json.load(users_file)

        def iterator():
            for x in users:
                print(x)
                for y in x:
                    print(y)

        def user_lookup():
            for user_number in args:
                print("user Lookup")
                print("Your Phone #: ", user_number)
                print("First Name: ", users[user_number]["first_name"])
                print("Last Name: ", users[user_number]["last_name"])

        if "iterate" in args:
            return iterator()
        elif "all" in args:
            return users
        else:
            response = user_lookup()
            return response

    def check_in(*args, users=users):
        # for user_number in args:
            # - Work in progress: The following code works, but it currently does not dynamically give back the individual's information. It only replies with "Esteemed + Caregiver".
            # first_name = str(users[user_number]["first_name"])
            # last_name = str(users[user_number]["last_name"])
            # return "You have successfully checked in, " + first_name + " " + last_name + "!"
            # return "You have successfully checked in!"
        return "You have successfully checked in!"


# - Run
if __name__ == "__main__":
    # - Debugging
    # print("")
    # fake_user_input = "+18509827871"
    # Companyusers.users(fake_user_input)

    # - Debugging
    print("")
    Users.get_users()
