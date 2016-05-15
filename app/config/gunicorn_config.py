# - Note: The reason for making this file is that I was trying to solve the following error:
# sqlalchemy.exc.OperationalError: (OperationalError) SSL error: decryption failed or bad record mac
# Heroku describes the problem further - https://devcenter.heroku.com/articles/forked-pg-connections

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
