from app.models import db, AppConfig, Modules, OmsConfig, CrmConfig, HrmConfig, AmsConfig, MmsConfig, User, Roles, Permissions, AppNotifications
# from app.routes import Violations
from app.config import sk_generator
# from psycopg2 import IntegrityError
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import update

### Notes ###
# The following code is an example of a way that works to update a db value.
# user = User.query.filter_by(id='9').update(dict(username='newname'))

integrity_error = "* IntegrityError: (({})) - Exception occurred while trying to add 1+ default sets of values. Perhaps they already exist."
errors = []

# DB creation.
# - Creates DB schema if it does not already exist.
db.create_all()


def add_rows_to_config_table(table_name, table_class, table_rows):
    commit_errors = False
    for key, value, permission_level, active in table_rows:
        try:
            db.session.add(table_class(key, value, permission_level, active))
            db.session.commit()
        except:
            commit_errors = True
            db.session.rollback()
    if commit_errors == True:
        errors.append(integrity_error.format(table_name))

# App config initialization.
# IMPORTANT! - Post-deployment, you will want to make sure that you change the secret key value in your database.
app_config_rows = [["App Name", "Just-a-Dash", 1, True],
    ["App Icon", "glyphicon glyphicon-equalizer", 1, True],
    ["App Title", "Just-a-Dash Enterprise Management System", 1, True],
    ["App Short-Title", "Just-a-Dash", 1, True],
    ["Toggle Placeholders", "false", 1, True],
    ["Secret Key", sk_generator(size=24), 1, True]]
add_rows_to_config_table('App Config', AppConfig, app_config_rows)


# Module registry initialization.
# - By default, Just-a-Dash comes with the following pre-built modules: Operations, Customer Relations, Human Resources, Accounting, Marketing
modules_rows = [["Admin Control Panel", "App", "Administrative control panel.", True],
    ["Operations", "OMS", "Operations management system.", True],
    ["Customer Relations", "CRM", "Customer relationship management system.", True],
    ["Human Resources", "HRM", "Human resource management system.", True],
    ["Accounting", "AMS", "Accounting management system.", True],
    ["Marketing", "MMS", "Marketing management system.", True]]
add_rows_to_config_table('Modules', Modules, modules_rows)


# Module config initializations.
# - OMS
oms_config_rows = [["Module Name", "Operations", 1, True],
    ["Module Abbreviation", "OMS", 1, True],
    ["Module Icon", "fa fa-fort-awesome", 1, True],
    ["Module Title", "Operations Management System", 1, True],
    ["Module Short-Title", "Operations Management", 1, True],
    ["Twilio Account SID", "", 1, True],
    ["Twilio Auth Token", "", 1, True],
    ["Twilio Phone Number", "+10000000000", 1, True],
    ["Phone Number Visibility", 'false', 1, True],
    ["Call Response MP3", 'http://www.you-should-upload-an-mp3-to-some-file-storage-and-then-enter-the-url-address-here.com/some_sound_file.mp3', 1, True],
    ["Call Response MP3 Toggle", 'false', 1, True],
    ["Call Response Text-to-Speech", 'You have successfully checked in. Thank you, and have a wonderful day!', 1, True],
    ["Call Response Text-to-Speech Toggle", 'true', 1, True]]
add_rows_to_config_table('OMS Module Config', OmsConfig, oms_config_rows)


# - CRM
crm_config_rows = [["Module Name", "Customer Relations", 1, True],
    ["Module Abbreviation", "", 1, True],
    ["Module Icon", "ion-person-stalker", 1, True],
    ["Module Title", "Customer Relationship Management System", 1, True],
    ["Module Short-Title", "Customer Relations Management", 1, True]]
add_rows_to_config_table('CRM Module Config', CrmConfig, crm_config_rows)


# - HRM
hrm_config_rows = [["Module Name", "Human Resources", 1, True],
    ["Module Abbreviation", "", 1, True],
    ["Module Icon", "fa fa-users", 1, True],
    ["Module Title", "Human Resource Management System", 1, True],
    ["Module Short-Title", "Human Resources Management", 1, True]]
add_rows_to_config_table('HRM Module Config', HrmConfig, hrm_config_rows)


# - AMS
ams_config_rows = [["Module Name", "Accounting", 1, True],
    ["Module Abbreviation", "", 1, True],
    ["Module Icon", "fa fa-bar-chart", 1, True],
    ["Module Title", "Accounting Management System", 1, True],
    ["Module Short-Title", "Accounting Management", 1, True]]
add_rows_to_config_table('AMS Module Config', AmsConfig, ams_config_rows)


# - MMS
mms_config_rows = [["App Name", "Marketing", 1, True],
    ["Module Abbreviation", "", 1, True],
    ["App Icon", "fa fa-line-chart", 1, True],
    ["App Title", "Marketing Management System", 1, True],
    ["App Short-Title", "Marketing Management", 1, True]]
add_rows_to_config_table('MMS Module Config', MmsConfig, mms_config_rows)


# Default users initialization.
# - Initalizes the app with a user with master permissions. The app administrator should change the e-mail/password immediately. Also adds a basic admin and a basic user.
# - IMPORTANT! - Post-deployment, you will want to make sure that you change these passwords (at least for 'master') in your database.
# - Note: The below code seemed necessary when using Bcrypt, but am not using Werkzeug Security.
# for item in db.session:
#     item.password = item.password.decode("utf-8")
user_rows = [["master", "master@not-a-real-email.com", "master", "master", "master", "master", "master", "master", "master"],
    ["super_admin", "super@not-a-real-email.com", "super_admin", "super", "super", "super", "super", "super", "super"],
    ["admin", "admin@not-a-real-email.com", "admin", "basic", "basic", "basic", "basic", "basic", "basic"],
    ["user", "user@not-a-real-email.com", "user", "None", "None", "None", "None", "None", "None"],
    ["demo", "demo@not-a-real-email.com", "demo", "basic", "basic", "basic", "basic", "basic", "basic"],
    ["oms_demo", "oms_demo@not-a-real-email.com", "oms_demo", "None", "basic", "None", "None", "None", "None"],
    ["crm_demo", "crm_demo@not-a-real-email.com", "crm_demo", "None", "None", "basic", "None", "None", "None"],
    ["hrm_demo", "hrm_demo@not-a-real-email.com", "hrm_demo", "None", "None", "None", "basic", "None", "None"],
    ["ams_demo", "ams_demo@not-a-real-email.com", "ams_demo", "None", "None", "None", "None", "basic", "None"],
    ["mms_demo", "mms_demo@not-a-real-email.com", "mms_demo", "None", "None", "None", "None", "None", "basic"]]
user_errors = False
for username, email, password, admin_role, oms_role, crm_role, hrm_role, ams_role, mms_role in user_rows:
    try:
        db.session.add(User(username, email, password, admin_role, oms_role, crm_role, hrm_role, ams_role, mms_role))
        db.session.commit()
    except:
        user_errors = True
        db.session.rollback()
if user_errors == True:
    errors.append(integrity_error.format('Users'))


# Roles initialization.
# - Initializes the app with admin/group roles.
roles_rows = [["App", "Master", 0],
    ["App", "Super", 1],
    ["App", "Basic", 2],
    ["App", "Custom1", 777],
    ["OMS", "Master", 0],
    ["OMS", "Super", 1],
    ["OMS", "Basic", 2],
    ["OMS", "Custom1", 777],
    ["CRM", "Master", 0],
    ["CRM", "Super", 1],
    ["CRM", "Basic", 2],
    ["CRM", "Custom1", 777],
    ["HRM", "Master", 0],
    ["HRM", "Super", 1],
    ["HRM", "Basic", 2],
    ["HRM", "Custom1", 777],
    ["AMS", "Master", 0],
    ["AMS", "Super", 1],
    ["AMS", "Basic", 2],
    ["AMS", "Custom1", 777],
    ["MMS", "Master", 0],
    ["MMS", "Super", 1],
    ["MMS", "Basic", 2],
    ["MMS", "Custom1", 777]]
roles_errors = False
for module_abbreviation, role, permission_level in roles_rows:
    try:
        db.session.add(Roles(module_abbreviation, role, permission_level))
        db.session.commit()
    except:
        roles_errors = True
        db.session.rollback()
if roles_errors == True:
    errors.append(integrity_error.format('Roles'))


# Permissions initialization.
# - Initializes the app with admin roles.
# Parameters: module, role, permission, r(read), w(write), u(update), d(delete).
permissions_rows = [["App", "Master", "Master_All", True, True, True, True],
    ["App", "Super", "Super_All", True, True, True, True],
    ["App", "Basic", "Read_Only", True, False, False, False],
    ["App", "Read", "Can_Read", True, False, False, False],
    ["App", "Write", "Can_Write", False, True, False, False],
    ["App", "Update", "Can_Update", False, False, True, False],
    ["App", "Delete", "Can_Delete", False, False, False, True],
    ["OMS", "Master", "Master_All", True, True, True, True],
    ["OMS", "Super", "Super_All", True, True, True, True],
    ["OMS", "Basic", "Read_Only", True, False, False, False],
    ["OMS", "Read", "Can_Read", True, False, False, False],
    ["OMS", "Write", "Can_Write", False, True, False, False],
    ["OMS", "Update", "Can_Update", False, False, True, False],
    ["OMS", "Delete", "Can_Delete", False, False, False, True],
    ["CRM", "Master", "Master_All", True, True, True, True],
    ["CRM", "Super", "Super_All", True, True, True, True],
    ["CRM", "Basic", "Read_Only", True, False, False, False],
    ["CRM", "Read", "Can_Read", True, False, False, False],
    ["CRM", "Write", "Can_Write", False, True, False, False],
    ["CRM", "Update", "Can_Update", False, False, True, False],
    ["CRM", "Delete", "Can_Delete", False, False, False, True],
    ["HRM", "Master", "Master_All", True, True, True, True],
    ["HRM", "Super", "Super_All", True, True, True, True],
    ["HRM", "Basic", "Read_Only", True, False, False, False],
    ["HRM", "Read", "Can_Read", True, False, False, False],
    ["HRM", "Write","Can_Write", False, True, False, False],
    ["HRM", "Update", "Can_Update", False, False, True, False],
    ["HRM", "Delete", "Can_Delete", False, False, False, True],
    ["AMS", "Master", "Master_All", True, True, True, True],
    ["AMS", "Super", "Super_All", True, True, True, True],
    ["AMS", "Basic", "Read_Only", True, False, False, False],
    ["AMS", "Read", "Can_Read", True, False, False, False],
    ["AMS", "Write", "Can_Write", False, True, False, False],
    ["AMS", "Update", "Can_Update", False, False, True, False],
    ["AMS", "Delete", "Can_Delete", False, False, False, True],
    ["MMS", "Master", "Master_All", True, True, True, True],
    ["MMS", "Super", "Super_All", True, True, True, True],
    ["MMS", "Basic", "Read_Only", True, False, False, False],
    ["MMS", "Read", "Can_Read", True, False, False, False],
    ["MMS", "Write", "Can_Write", False, True, False, False],
    ["MMS", "Update", "Can_Update", False, False, True, False],
    ["MMS", "Delete", "Can_Delete", False, False, False, True]]
permissions_errors = False
for module, role, permission, r, w, u, d in permissions_rows:
    try:
        db.session.add(Permissions(module, role, permission, r, w, u, d))
        db.session.commit()
    except:
        permissions_errors = True
        db.session.rollback()
if permissions_errors == True:
    errors.append(integrity_error.format('Permissions'))


# Tutorial messages initialization.
# - Initializes the database creation with a first message to start the user off with an app tutorial.
notifications_rows = [["Notification", "Tutorial", "Welcome to Just-a-Dash!",
    "Welcome to Just-a-Dash, the minimalist's dashboard application. I hope that you enjoy your experience. To get in "
    "touch with me for comment / question / feature request / whatever it may be, feel free to e-mail "
    "joeflack4@gmail.com, or check out my blog, joeflack.net. - Joe Flack, Creator of Just-a-Dash",
    "Joe Flack", "Group:AllUsers", "WebApp, NativeApps, Email"]]
notifications_errors = False
for message_type, subcategory, title, body, author, destinations, delivery_methods in notifications_rows:
    try:
        db.session.add(AppNotifications(message_type, subcategory, title, body, author, destinations, delivery_methods))
        db.session.commit()
    except:
        notifications_errors = True
        db.session.rollback()
if notifications_errors == True:
    errors.append(integrity_error.format('App Notifications'))

# - Summary
print("")
print("# # # Database creation and initialization complete. # # #")
print("")
if len(errors) > 0:
    print("Summary of exceptions: ")
    for error in errors:
        print(error)
    print("")
