from app.models import *
# from psycopg2 import IntegrityError
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import update

### Notes ###
# The following code is an example of a way that works to update a db value.
# user = User.query.filter_by(id='9').update(dict(username='newname'))

integrity_error = "* IntegrityError: {} - Exception occurred while trying to add 1+ default sets of values. Perhaps they already exist."
errors = []

# DB creation.
# - Creates DB schema if it does not already exist.
db.create_all()

# Module registry initialization.
# - By default, Just-a-Dash comes with the following pre-built modules: Operations, Customer Relations, Human Resources, Accounting, Marketing
try:
    db.session.add(Modules("Admin Control Panel", "ACP", "Administrative control panel.", True))
    db.session.add(Modules("Operations", "OMS", "Operations management system.", True))
    db.session.add(Modules("Customer Relations", "CRM", "Customer relationship management system.", True))
    db.session.add(Modules("Human Resources", "HRM","Human resource management system.", True))
    db.session.add(Modules("Accounting", "AMS", "Accounting management system.", True))
    db.session.add(Modules("Marketing", "MMS", "Marketing management system.", True))
    db.session.commit()
except:
    errors.append(integrity_error.format("Modules"))
    db.session.rollback()

# Default users initialization.
# - Initalizes the app with a user with master permissions. The app administrator should change the e-mail/password immediately. Also adds a basic admin and a basic user.
# - The domain shown here is simply a randomly generated 10-digit string.
try:
    # db.session.add(User("master", "master@not-a-real-email.com", "master", "master", "super", "super", "super", "super", "super"))
    # db.session.add(User("super_admin", "super@not-a-real-email.com", "super_admin", "super", "super", "super", "super", "super", "super"))
    # db.session.add(User("admin", "admin@not-a-real-email.com", "admin", "basic", "basic", "basic", "basic", "basic", "basic"))
    # db.session.add(User("user", "user@not-a-real-email.com", "user", "None", "None", "None", "None", "None", "None"))
    db.session.add(User("demo", "demo@not-a-real-email.com", "demo", "basic", "basic", "basic", "basic", "basic", "basic"))
    db.session.add(User("oms_demo", "oms_demo@not-a-real-email.com", "oms_demo", "None", "basic", "None", "None", "None", "None"))
    db.session.add(User("crm_demo", "crm_demo@not-a-real-email.com", "crm_demo", "None", "None", "basic", "None", "None", "None"))
    db.session.add(User("hrm_demo", "hrm_demo@not-a-real-email.com", "hrm_demo", "None", "None", "None", "basic", "None", "None"))
    db.session.add(User("ams_demo", "ams_demo@not-a-real-email.com", "ams_demo", "None", "None", "None", "None", "basic", "None"))
    db.session.add(User("mms_demo", "mms_demo@not-a-real-email.com", "mms_demo", "None", "None", "None", "None", "None", "basic"))

    # - The below code seemed necessary when using Bcrypt, but am not using Werkzeug Security.
    # for item in db.session:
    #     item.password = item.password.decode("utf-8")

    db.session.commit()
# except IntegrityError as e:
except:
    errors.append(integrity_error.format("Users"))
    db.session.rollback()

# Roles initialization.
# - Initializes the app with admin/group roles.
try:
    db.session.add(Roles("Master", "ACP"))
    db.session.add(Roles("Super", "ACP"))
    db.session.add(Roles("Basic", "ACP"))
    db.session.add(Roles("Custom1", "ACP"))
    db.session.add(Roles("Master", "OMS"))
    db.session.add(Roles("Super", "OMS"))
    db.session.add(Roles("Basic", "OMS"))
    db.session.add(Roles("Custom1", "OMS"))
    db.session.add(Roles("Master", "CRM"))
    db.session.add(Roles("Super", "CRM"))
    db.session.add(Roles("Basic", "CRM"))
    db.session.add(Roles("Custom1", "CRM"))
    db.session.add(Roles("Master", "HRM"))
    db.session.add(Roles("Super", "HRM"))
    db.session.add(Roles("Basic", "HRM"))
    db.session.add(Roles("Custom1", "HRM"))
    db.session.add(Roles("Master", "AMS"))
    db.session.add(Roles("Super", "AMS"))
    db.session.add(Roles("Basic", "AMS"))
    db.session.add(Roles("Custom1", "AMS"))
    db.session.add(Roles("Master", "MMS"))
    db.session.add(Roles("Super", "MMS"))
    db.session.add(Roles("Basic", "MMS"))
    db.session.add(Roles("Custom1", "MMS"))
    db.session.commit()
except:
    errors.append(integrity_error.format("Roles"))
    db.session.rollback()

# Permissions initialization.
# - Initializes the app with admin roles.
try:
    db.session.add(Permissions("Master", "ACP", "Master_All", True, True, True, True))
    db.session.add(Permissions("Super", "ACP", "Super_All", True, True, True, True))
    db.session.add(Permissions("Basic", "ACP", "Read_Only", True, False, False, False))
    db.session.add(Permissions("Read", "ACP", "Can_Read", True, False, False, False))
    db.session.add(Permissions("Write", "ACP", "Can_Write", False, True, False, False))
    db.session.add(Permissions("Update", "ACP", "Can_Update", False, False, True, False))
    db.session.add(Permissions("Delete", "ACP", "Can_Delete", False, False, False, True))

    db.session.add(Permissions("Master", "OMS", "Master_All", True, True, True, True))
    db.session.add(Permissions("Super", "OMS", "Super_All", True, True, True, True))
    db.session.add(Permissions("Basic", "OMS", "Read_Only", True, False, False, False))
    db.session.add(Permissions("Read", "OMS", "Can_Read", True, False, False, False))
    db.session.add(Permissions("Write", "OMS", "Can_Write", False, True, False, False))
    db.session.add(Permissions("Update", "OMS", "Can_Update", False, False, True, False))
    db.session.add(Permissions("Delete", "OMS", "Can_Delete", False, False, False, True))

    db.session.add(Permissions("Master", "CRM", "Master_All", True, True, True, True))
    db.session.add(Permissions("Super", "CRM", "Super_All", True, True, True, True))
    db.session.add(Permissions("Basic", "CRM", "Read_Only", True, False, False, False))
    db.session.add(Permissions("Read", "CRM", "Can_Read", True, False, False, False))
    db.session.add(Permissions("Write", "CRM", "Can_Write", False, True, False, False))
    db.session.add(Permissions("Update", "CRM", "Can_Update", False, False, True, False))
    db.session.add(Permissions("Delete", "CRM", "Can_Delete", False, False, False, True))

    db.session.add(Permissions("Master", "HRM", "Master_All", True, True, True, True))
    db.session.add(Permissions("Super", "HRM", "Super_All", True, True, True, True))
    db.session.add(Permissions("Basic", "HRM", "Read_Only", True, False, False, False))
    db.session.add(Permissions("Read", "HRM", "Can_Read", True, False, False, False))
    db.session.add(Permissions("Write", "HRM", "Can_Write", False, True, False, False))
    db.session.add(Permissions("Update", "HRM", "Can_Update", False, False, True, False))
    db.session.add(Permissions("Delete", "HRM", "Can_Delete", False, False, False, True))

    db.session.add(Permissions("Master", "AMS", "Master_All", True, True, True, True))
    db.session.add(Permissions("Super", "AMS", "Super_All", True, True, True, True))
    db.session.add(Permissions("Basic", "AMS", "Read_Only", True, False, False, False))
    db.session.add(Permissions("Read", "AMS", "Can_Read", True, False, False, False))
    db.session.add(Permissions("Write", "AMS", "Can_Write", False, True, False, False))
    db.session.add(Permissions("Update", "AMS", "Can_Update", False, False, True, False))
    db.session.add(Permissions("Delete", "AMS", "Can_Delete", False, False, False, True))

    db.session.add(Permissions("Master", "MMS", "Master_All", True, True, True, True))
    db.session.add(Permissions("Super", "MMS", "Super_All", True, True, True, True))
    db.session.add(Permissions("Basic", "MMS", "Read_Only", True, False, False, False))
    db.session.add(Permissions("Read", "MMS", "Can_Read", True, False, False, False))
    db.session.add(Permissions("Write", "MMS", "Can_Write", False, True, False, False))
    db.session.add(Permissions("Update", "MMS", "Can_Update", False, False, True, False))
    db.session.add(Permissions("Delete", "MMS", "Can_Delete", False, False, False, True))

    db.session.commit()
except:
    errors.append(integrity_error.format("Permissions"))
    db.session.rollback()

# What to do here?
# - Takes the previously added users, and sets their roles.

# X initialization.
# - Initializes the app with X.

db.session.commit()

# X initialization.
# - Initializes the app with X.

db.session.commit()

# Tutorial messages initialization.
# - Initializes the database creation with a first message to start the user off with an app tutorial.
try:
    db.session.add(AppNotifications("Notification",
                            "Tutorial",
                            "Welcome to Just-a-Dash!",
                            "Welcome to Just-a-Dash, the minimalist's dashboard application. I hope that you enjoy your experience. To get in touch with me for comment / question / feature request / whatever it may be, feel free to e-mail joeflack4@gmail.com, or check out my blog, joeflack.net. - Joe Flack, Creator of Just-a-Dash",
                            "Joe Flack",
                            "Group:AllUsers",
                            "WebApp, NativeApps, Email"))
    db.session.commit()
except:
    errors.append(integrity_error.format("App Notifications"))
    db.session.rollback()

# - Summary
print("")
print("# # # Database creation and initialization complete. # # #")
print("")
print("Summary of exceptions: ")
for error in errors:
    print(error)
print("")
