import unittest
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from alembic.runtime.environment import EnvironmentContext
from app import app, db
# import os
# app.config.from_object(os.environ['APP_SETTINGS'])

env = EnvironmentContext.configure
# This will allow migrations to listen to column type changes.
env.compare_type = True

print("")
print("# # # Running DB Manager, using Alembic and Flask-Migrate. # # #")
print("# # # DB: '", app.config['SQLALCHEMY_DATABASE_URI'], "' # # #")

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1

if __name__ == '__main__':
    manager.run()
