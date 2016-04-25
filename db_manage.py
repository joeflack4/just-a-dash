from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from alembic.runtime.environment import EnvironmentContext
from app import app, db
# import os
# app.config.from_object(os.environ['APP_SETTINGS'])

env = EnvironmentContext.configure
# This will allow migrations to listen to column type changes.
env.compare_type=True

print("")
print("# # # Running DB Manager, using Alembic and Flask-Migrate. # # #")
print("# # # DB: '", app.config['SQLALCHEMY_DATABASE_URI'], "' # # #")

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
