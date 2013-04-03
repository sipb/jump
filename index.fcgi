#!/usr/bin/python
# import os
# import sys
# curdir = os.path.dirname(os.path.realpath(__file__))
# sys.path.insert(0, curdir + '/venv/lib/python2.7/site-packages')

from flup.server.fcgi import WSGIServer
from jump import app

class ScriptNameStripper(object):
   def __init__(self, app):
       self.app = app

   def __call__(self, environ, start_response):
       environ['SCRIPT_NAME'] = ''
       environ['HTTPS'] = 'false'
       return self.app(environ, start_response)

app = ScriptNameStripper(app)

if __name__ == '__main__':
    WSGIServer(app).run()
