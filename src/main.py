# import set_sys_path is needed here although it appears not to be used
# we were having problem on appengine one day that it couldn't import webapp2, located in lib
# after adding this line, the app works.
import set_sys_path

import webapp2
from config import DEBUG
from urls import routes
import config

def enable_jinja2_debugging():
    """Enables blacklisted modules that help Jinja2 debugging.
        regarding the ImportError, read:
        http://jinja.pocoo.org/docs/faq/#my-tracebacks-look-weird-what-s-happening
    """
    if not DEBUG:
        return
    try:
        from google.appengine.tools.dev_appserver import HardenedModulesHook
        HardenedModulesHook._WHITE_LIST_C_MODULES += ['_ctypes', 'gestalt']
    except ImportError:
        pass # not available on production environment, but we may still want DEBUG on

config = config.CONFIG

APP = webapp2.WSGIApplication(routes=routes, debug=True, config=config)
enable_jinja2_debugging()

# set up the custom error handlers
from app.views import errors
APP.error_handlers[404] = errors.Handle404()
APP.error_handlers[500] = errors.Handle500()