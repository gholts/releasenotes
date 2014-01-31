from app.views.jinja_ext.vurl import do_vurl
from app.views.jinja_ext.util import do_bookend, do_re_sub, do_substring, do_dateformat, do_datetimeformat, \
    do_spliturlhost
from webapp2 import uri_for
import os
current_path = os.path.abspath(os.path.dirname(__file__))

ENVIRON_CONFIG = {}

# configuration for sessions
SESSION_COOKIE_NAME = 'session'
CONFIG = {
    'web_settings'   : {
        'ssl_enabled': False
    },
    'webapp2_extras.jinja2' : {
        'filters' : {
            'vurl' :        do_vurl,
            'bookend' :     do_bookend,
            're_sub' :      do_re_sub,
            'substring' :   do_substring,
            'dateformat' :  do_dateformat,
            'datetimeformat' :  do_datetimeformat,
            'splithost' : do_spliturlhost
        },
        'globals'   : {
            'uri_for': uri_for
        },
        'template_path': os.path.join(current_path, 'templates')
    },
    'webapp2_extras.sessions' : {
        'secret_key': 'some-secret-key', #CHANGE ME
        'cookie_name': SESSION_COOKIE_NAME,
        'backends': {
            'datastore': 'webapp2_extras.appengine.sessions_ndb.DatastoreSessionFactory',
            'memcache': 'webapp2_extras.appengine.sessions_memcache.MemcacheSessionFactory',
            'securecookie': 'webapp2_extras.sessions.SecureCookieSessionFactory'
        }
    }
}
ENVIRONMENT_NAME = ""

# DEBUG and STATIC_VERSION_NUMBER should be updated when deploying to production environment.
# Set STATIC_VERSION_NUMBER to None to disable static caching
DEBUG = True
STATIC_VERSION_NUMBER = 1

try:
    # pylint: disable=W0401
    # W0401: 19: Wildcard import config_local
    from config_local import *
    CONFIG.update(ENVIRON_CONFIG)
except ImportError:
    import logging
    logging.debug("No config_local.py, using config.py only.")
