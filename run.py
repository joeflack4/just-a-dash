#!/usr/bin/env python
# Under normal circumstances, this script would not be necessary. The sample_application would have its own setup.py and be properly installed;
# However since it is not bundled in the sdist package, we need some hacks to make it work.
import os
import sys
sys.path.append(os.path.dirname(__name__))
from app import app


app.run(debug=True)
print("")
print("##### Just-a-Dash ERP Dashboard #####")
