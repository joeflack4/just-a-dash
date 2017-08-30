#!/usr/bin/env python
"""Run."""
import os
import sys
from justadash import app

sys.path.append(os.path.dirname(__name__))

app.run(debug=True, port=8080)
print("")
print("##### Just-a-Dash ERP Dashboard #####")
