""" Handler for index urls. """

from app.views import BaseHandler

class IndexView(BaseHandler):
    """ Handles the root url. """
    def get(self):
        """ GET """
        self.render_response('index.html')