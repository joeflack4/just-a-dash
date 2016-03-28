from app import db
from app.models import *

db.create_all()

db.session.add(User("admin", "ad@min.com", "admin"))

# Initializes the database creation with a first message.
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
