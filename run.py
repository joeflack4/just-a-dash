#!/usr/bin/env python
# under normal circumstances, this script would not be necessary. the
# sample_application would have its own setup.py and be properly installed;
# however since it is not bundled in the sdist package, we need some hacks
# to make it work

import os
import sys
sys.path.append(os.path.dirname(__name__))
from app import app


# AdminLTE Boilerplate #
# create an app instance
#app = app()


print("")
print("##### Just-a-Dash ERP Dashboard #####")
app.run(debug=True)
