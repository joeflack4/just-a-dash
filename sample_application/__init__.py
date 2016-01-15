#!/usr/bin/env python
from flask import Flask, render_template
from flask_adminlte import AdminLTE


def create_app(configfile=None):
    app = Flask(__name__)
    AdminLTE(app)

    @app.route('/')
    def index():
        test_var = "I <3 Ashley"
        return render_template('index.html',
		                      test_var=test_var)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
