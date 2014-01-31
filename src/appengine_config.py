from google.appengine.ext.appstats import recording

from settings import DEBUG

def webapp_add_wsgi_middleware(app):
    if not DEBUG:
        return app
    app = recording.appstats_wsgi_middleware(app)
    return app
