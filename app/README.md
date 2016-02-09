# Just-a-Dash
![Just-a-Dash ERP Dashboard](http://joeflack.net/wp-content/uploads/2016/02/Just-a-Dash_Alpha01.png)
Just-a-Dash application is a light-weight, mobile friendly, scaffolded EMS (Enterprise Management System) platform. For our purposes, EMS is synonymous with the more common term 'ERP' (Enterprise Resource Planning).

#### Architecture
Just-a-Dash uses a highly modular SOA (Service Oriented Architecture) on both the front and back ends. The technology stack is as follows,

#### Documentation
As of right now, no user or development documentation exists. But it will.

#### Contributing
Contribution is encouraged. While Just-a-Dash's documentation is currently sparse, it is however straightforward and easy to learn, and the technologies it is built on are robust and well documented. Feel free to reach out to me, and I will assist in any way possible.

- Data Storage:  Your choice of RDBMS.
- Server Languages/Frameworks: *Python*, with MVC in *Flask*.
- Client Languages/Frameworks: HTML/CSS/JS, with UI in *Bootstrap*, themed with *AdminLTE*.

## Installation
#### Local Installation
The recommended method is `virtualenv`, with `pip`. The included `requirements.txt` lists dependencies, and is used by `virtualenv`, and *Heroku* (if deploying online) for installation of these dependencies. I highly recommend [The Flask Mega Tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) , Part I (& onwards) of which can be used as a guide for installation of this application.

#### Online Deployment
I recommend *Heroku* as a PaaS. If using Heroku, it will utilize the included `requirements.txt` file and `Procfile` to build and run your application.

## EMS Modules
#### Released Modules
Currently none.

#### Modules in Development
- HRM (Human Resources Management System)
- OMS (Operations Management System)
- DES (Data Extrapolation System)
- CRM (Customer Relationship Management)
- BMS (Billing Management System)
- Interface for External AMS (Accounting Management Systems)

## Screenshots
![Mobile Alpha 01](http://joeflack.net/wp-content/uploads/2016/02/JustADash_Alpha01-337x600.png)
