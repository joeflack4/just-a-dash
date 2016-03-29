from app import db
from sqlalchemy import update
from app.models import *

### Notes ###
# The following code is an example of a way that works to update a db value.
# user = User.query.filter_by(id='9').update(dict(username='newname'))

db.create_all()
# Keep this - Helps start a newly deployed app.
# db.session.add(User("admin", "ad@min.com", "admin".encode('utf-8')))
db.session.add(User("test16", "test16@gmail.com", "test"))
for item in db.session:
    item.password = item.password.decode("utf-8")


# Keep this - Helps start tutorial.
# Initializes the database creation with a first message.
# Messages Fields: type, subcategory, title, body, author, destinations, delivery_methods, notes.
# db.session.add(Messages("Notification",
#                         "Tutorial",
#                         "Welcome to Just-a-Dash!",
#                         "Welcome to Just-a-Dash, the minimalist's dashboard application. I hope that you enjoy your experience. To get in touch with me for comment / question / feature request / whatever it may be, feel free to e-mail joeflack4@gmail.com, or check out my blog, joeflack.net. - Joe Flack, Creator of Just-a-Dash",
#                         "Joe Flack",
#                         "Group:AllUsers",
#                         "WebApp, NativeApps, Email",
#                         ""
#                         ))


# - Debugging
# db.session.add(User("test6", "test6@gmail.com", bcrypt.generate_password_hash(u'test')))
# db.session.add(User("test16", "test16@gmail.com", "test"))
# for item in db.session:
#     print(item.password.decode("utf-8"))

# THIS MIGHT WORK
# db.session.add(User("test16", "test16@gmail.com", "test"))
# for item in db.session:
#     print(item.password)
#     item.password = item.password.decode("utf-8")
#     print(item.password)




# - Debugging
# user = User.query.filter_by(id='9').first()
# print(user.password)
# user.password = bcrypt.generate_password_hash(u'hunter2')
# print(user.password)
# user.name = "newname"
# user.update(dict(name='newname'))
# user.update(username='newname')

# pw_hash = bcrypt.generate_password_hash(u'hunter2')
# print(bcrypt.check_password_hash(pw_hash, 'hunter2')) # returns True



# Keep this.
db.session.commit()