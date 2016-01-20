*Vanillerp*
This application is a light-weight, mobile friendly, scaffolded EMS (Enterprise Management System) platform. For our purposes, EMS is synonymous with the more common term 'ERP' (Enterprise Resource Planning).

*Architecture*
Vanillerp uses a highly modular SOA (Service Oriented Architecture) on both the front and back ends. The technology stack is as follows,

Datbabase - Your choice of RDBMS.
Server Languages/Frameworks - Python, with MVC in Flask.
Client Languages/Frameworks - HTML/CSS/JS, with UI in Bootstrap, themed with AdminLTE.

*Installation*
For local installation, the recommended method is virtualenv, with pip. The included requirements.txt lists dependencies, and is used by virtualenv, and Heroku (if deploying online) for installation of these dependencies. I highly recommend The Flask Mega Tutorial (http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) , Part I (& onwards) of which can be used as a guide for installation of this application. Once fully set up, you can use the included '

For online deployment, I recommend Heroku as a PaaS. If using Heroku, it will utilize the included requirements.txt file and Procfile to build and run your application.

*Documentation*
As of right now, no user or development documentation exists. But it will.

*Contributing*
Contribution is encouraged. While Vanillerp's documentation is currently sparse, it is however straightforward and easy to learn, and the technologies it is built on are robust and well documented. Feel free to reach out to me, and I will assist in any way possible.

*EMS Modules*
Released modules: Currently none.

Modules in development:
- HRM (Human Resources Management System)
- OMS (Operations Management System)
- DES (Data Extrapolation System)
- CRM (Customer Relationship Management)
- BMS (Billing Management System)
- Interface for External AMS (Accounting Management Systems)