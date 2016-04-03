from app.models import *
# from sqlalchemy import update

### Notes ###
# The following code is an example of a way that works to update a db value.
# user = User.query.filter_by(id='9').update(dict(username='newname'))

# DB creation.
# - Creates DB schema if it does not already exist.
db.create_all()

# Module registry initialization.
# - By default, Just-a-Dash comes with the following pre-built modules: Operations, Customer Relations, Human Resources, Accounting, Marketing
db.session.add(Modules("Admin Control Panel", "ACP", "Administrative control panel.", True))
db.session.add(Modules("Operations", "OMS", "Operations management system.", True))
db.session.add(Modules("Customer Relations", "CRM", "Customer relationship management system.", True))
db.session.add(Modules("Human Resources", "HRM","Human resource management system.", True))
db.session.add(Modules("Accounting", "AMS", "Accounting management system.", True))
db.session.add(Modules("Marketing", "MMS", "Marketing management system.", True))
db.session.commit()

# Default users initialization.
# - Initalizes the app with a user with master permissions. The app administrator should change the e-mail/password immediately. Also adds a basic admin and a basic user.
# - The domain shown here is simply a randomly generated 10-digit string.
db.session.add(User("master", "master@x30pK9d2DF.com", "master"))
db.session.add(User("admin", "admin@x30pK9d2DF.com", "admin"))
db.session.add(User("user", "user@x30pK9d2DF.com", "user"))
for item in db.session:
    item.password = item.password.decode("utf-8")
db.session.commit()

# Roles initialization.
# - Initializes the app with admin/group roles.
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

# Permissions initialization.
# - Initializes the app with admin roles.
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

# What to do here?
# - Takes the previously added users, and sets their roles.

# X initialization.
# - Initializes the app with X.

db.session.commit()

# X initialization.
# - Initializes the app with X.

db.session.commit()

# Tutorial initialization.
# - Initializes the database creation with a first message to start the user off with an app tutorial.
# Messages Fields: type, subcategory, title, body, author, destinations, delivery_methods, notes.
db.session.add(Messages("Notification",
                        "Tutorial",
                        "Welcome to Just-a-Dash!",
                        "Welcome to Just-a-Dash, the minimalist's dashboard application. I hope that you enjoy your experience. To get in touch with me for comment / question / feature request / whatever it may be, feel free to e-mail joeflack4@gmail.com, or check out my blog, joeflack.net. - Joe Flack, Creator of Just-a-Dash",
                        "Joe Flack",
                        "Group:AllUsers",
                        "WebApp, NativeApps, Email",
                        ""
                        ))
db.session.commit()
