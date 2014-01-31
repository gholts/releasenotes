""" Handles warmup requests """

def warmup():
    """ Imports a bunch of stuff into memory. """

    import Cookie
    import StringIO
    import UserDict
    import UserList
    import UserString
    import base64
    import cgi
    import copy
    from copy import deepcopy
    import datetime
    import hmac
    import logging
    import md5
    import mimetools
    import mimetypes
    import pickle
    import random
    import re
    import sha
    import os, sys
    import time
    import types
    import urllib
    import urllib2
    from urllib2 import HTTPError
    from urllib import urlencode
    import urlparse
    import uuid

    import jinja2, simplejson, tinyid, webapp2, webapp2_extras, wtforms, webob
    from webapp2 import *
    from webapp2_extras import *
    from webapp2_extras.routes import *
    from jinja2 import *

    from __future__ import with_statement
    from ndb import model

    from wtforms import *
    from wtforms.fields import *
    from wtforms.widgets import *

    from google.appengine.api import datastore
    from google.appengine.api import images
    from google.appengine.api import mail
    from google.appengine.api import memcache
    from google.appengine.api import urlfetch
    from google.appengine.api import users
    from google.appengine.api import taskqueue
    from google.appengine.api import namespace_manager
    from google.appengine.api import apiproxy_stub_map
    from google.appengine.ext import bulkload
    from google.appengine.ext import db
    from google.appengine.ext import gql
    from google.appengine.ext import search
    from google.appengine.ext import webapp

    import set_sys_path

if __name__ == '__main__':
    warmup()