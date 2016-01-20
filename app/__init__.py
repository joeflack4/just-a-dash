#!/usr/bin/env python
from flask import Flask, render_template
from flask_adminlte import AdminLTE

app = Flask(__name__)
AdminLTE(app)

# AdminLTE Boilerplate #
#def create_app(configfile=None):
    #app = Flask(__name__)
    #AdminLTE(app)    
    

# Root Path
@app.route('/')
def index():
    page_header = "Welcome to the Pythonic Dashboard."
    return render_template('core_modules/dashboard/index.html',
                            page_header=page_header)

# Core Modules
@app.route('/dashboard')
def dashboard():
    page_header = "Welcome to the Pythonic Dashboard."
    return render_template('core_modules/dashboard/index.html',
		                    page_header=page_header)

@app.route('/account-settings')
def account_settings():
	return render_template('core_modules/account_settings/index.html')

@app.route('/app-settings')
def app_settings():
	return render_template('core_modules/app_settings/index.html')

@app.route('/login')
def login():
	return render_template('core_modules/login/index.html')

@app.route('/register')
def register():
	return render_template('core_modules/register/index.html')

@app.route('/profile')
def profile():
	return render_template('core_modules/profile/index.html')
						  
# Modules							  
@app.route('/hrm')
def hrm():
	return render_template('modules/hrm/index.html')

@app.route('/crm')
def crm():
	return render_template('modules/crm/index.html')	

@app.route('/operations')
def operations():
	return render_template('modules/operations/index.html')

@app.route('/accounting')
def accounting():
	return render_template('modules/accounting/index.html')	


# AdminLTE Boilerplate #	
    #return app

if __name__ == '__main__':
     app().run(debug=True)

# AdminLTE Boilerplate #	 
	#create_app().run(debug=True)