#!/usr/bin/env python
# under normal circumstances, this script would not be necessary. the
# sample_application would have its own setup.py and be properly installed;
# however since it is not bundled in the sdist package, we need some hacks
# to make it work

import os
import sys
sys.path.append(os.path.dirname(__name__))
from app import app, config

# AdminLTE Boilerplate #
# create an app instance
#app = app()






# Set app settings to detect and react to the type of environment being run.
# Isn't working at the moment.... Right now development environment will not be set.

# try:
#     app.config.from_object(os.environ['APP_SETTINGS'])
#     print(os.environ['APP_SETTINGS'])
# except KeyError as e:
#     # print("Exception: ", e, ": APP_SETTINGS not set. This may be your local development environment, or APP_SETTINGS has otherwise not been set on your test/staging/deployment environments.")
#     # print("Exception has been handled by automatic runtime setting of APP_SETTINGS value.")
#     os.environ["APP_SETTINGS"] = str(config.DevelopmentConfig)
#     # app.config.from_object(os.environ['APP_SETTINGS'])
#     app.config.from_object(config.DevelopmentConfig)
#     print(os.environ['APP_SETTINGS'])
# except:
#     # print("Error: Unexpected exception occured when trying to apply APP_SETTINGS. This may be your local development environment, or APP_SETTINGS has otherwise not been set on your test/staging/deployment environments.")
#     # print("Exception has been handled by automatic runtime setting of APP_SETTINGS value.")
#     os.environ["APP_SETTINGS"] = str(config.DevelopmentConfig)
#     app.config.from_object(config.DevelopmentConfig)
#     print(os.environ['APP_SETTINGS'])
#     pass




# print(os.environ['APP_SETTINGS'])

print("")
print("##### Just-a-Dash ERP Dashboard #####")
app.run(debug=True)
