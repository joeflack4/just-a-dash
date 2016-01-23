#!/usr/bin/env python
from flask import Flask
from flask_adminlte import AdminLTE

# - Initialize App
app = Flask(__name__)
from app import routes

# - Initialize UI Theme
AdminLTE(app)

# - Contingencies
# Run - Allows running of app directly from this file.
if __name__ == '__main__':
    app().run(debug=True)
