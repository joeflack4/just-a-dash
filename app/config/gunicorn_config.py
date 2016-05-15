# - Note: The reason for making this file is that I was trying to solve the following error:
# sqlalchemy.exc.OperationalError: (OperationalError) SSL error: decryption failed or bad record mac
# - More Notes:
# * The Problem - https://devcenter.heroku.com/articles/forked-pg-connections
# * Etc - http://stackoverflow.com/questions/36190763/celery-flask-sqlalchemy-databaseerror-databaseerror-ssl-error-decryption-f
# * Gunicorn Config - http://docs.gunicorn.org/en/stable/settings.html#config-file
# * More on Gunicorn Config - http://docs.gunicorn.org/en/stable/configure.html
# * Post Fork - http://docs.gunicorn.org/en/stable/settings.html#post-fork
# * Example to fix code - https://devcenter.heroku.com/articles/forked-pg-connections#unicorn-server
# - Solution: Rather than the more optimized, more complicated solution of keeping pre-loading, and simply closing
# db connection on pre-fork, etc, I simply turned off app pre-loading. This is not too bad if the app is small.

# - Note: Example code taken from - http://smellman.hatenablog.com/entry/2013/04/17/022148
# # -*- coding: utf-8 -*-
# bind = '127.0.0.1:5000'
# backlog = 2048
# ...
# debug = False
# spew  = False
# preload_app = True
# daemon = True
# pidfile = '/tmp/hoge_gunicorn.pid'
# user  = 'hoge'
# group = 'hoge'
# accesslog = '/var/log/gunicorn/hoge-access.log' # /var/log/gunicornを作成しておく
# errorlog = '/var/log/gunicorn/hoge-error.log'
# loglevel = 'info'
# logconfig = None

def pre_fork(server, worker):
    pass


def post_fork(server, worker):
    pass
