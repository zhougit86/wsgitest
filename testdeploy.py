'''
Created on 2013-10-28

@author: root
'''

import logging
import os
import sys
import webob
from webob import Request
from webob import Response
from webob.dec import *
from webob.exc import *

from paste.deploy import loadapp
from wsgiref.simple_server import make_server
import signal


# def sigint_handler(signal, frame):
#     """Exits at SIGINT signal."""
#     logging.debug('SIGINT received, stopping servers.')
#     sys.exit(0)


@wsgify
def test(request):
    return Response('Here!')



@wsgify
def application(request):
    return Response('Hello and Welcome!')



@wsgify.middleware
def auth_filter(request, app):
    if request.headers.get('X-Auth-Token') != 'bluefire1991':
        return test
    return app(request)

def filter_factory(global_conf, **local_conf):
    return auth_filter

# filter_factory
def filter_factory(global_conf, **local_conf):
    return auth_filter

# app_factory
def show_factory(global_conf, **local_conf):
    return application






# app_factory
def version_factory(global_conf, **local_conf):
    return ShowVersion(global_conf, local_conf)


# app_fatory
def showauther_factory(global_conf, **local_conf):
    return ShowAuther(global_conf, local_conf)


# filter_factory



# filter_factory
def log_factory(global_conf, **local_conf):
    def filter(app):
        return LogFilter(app, global_conf, local_conf)

    return filter


class LogFilter():
    def __init__(self, app, global_conf, local_conf):
        self.app = app
        self.global_conf = global_conf
        self.local_conf = local_conf

    def __call__(self, environ, start_response):
        print "filter:LogFilter is called."
        req = Request(environ)
        if req.GET.get("username", "") == self.local_conf['username'] and req.GET.get("password", "") == \
                self.local_conf['password']:
            return self.app(environ, start_response)
        start_response("200 OK", [("Content-type", "text/plain")])
        return ["You are not authorized"]


class ShowVersion():
    def __init__(self, global_conf, local_conf):
        self.global_conf = global_conf
        self.local_conf = local_conf

    def __call__(self, environ, start_response):
        start_response("200 OK", [("Content-type", "text/plain")])
        return ['Version', self.local_conf['version']]


class ShowAuther():
    def __init__(self, global_conf, local_conf):
        self.global_conf = global_conf
        self.local_conf = local_conf

    def __call__(self, environ, start_response):
        res = Response()
        res.status = "200 OK"
        res.content_type = "text/plain"
        # get operands
        res.body = ["auther", self.local_conf['auther']]
        return res



    # signal.signal(signal.SIGINT, sigint_handler)
configfile = "test-deploy.ini"
appname = "pdl"
wsgi_app = loadapp("config:%s" % os.path.abspath(configfile), appname)
server = make_server('localhost', 8088, wsgi_app)
server.serve_forever()
