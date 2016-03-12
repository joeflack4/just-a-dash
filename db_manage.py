from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

# import os
from app import app, db
# app.config.from_object(os.environ['APP_SETTINGS'])

print("")
print("# # # Running DB Manager, using Alembic and Flask-Migrate. # # #")
print("# # # DB: '", app.config['SQLALCHEMY_DATABASE_URI'], "' # # #")

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
