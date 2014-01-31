""" Handlers for custom error pages. """

import sys
import traceback
from app.views import BaseHandler

class ExceptionHandler(BaseHandler):
    """ Generic exception handler. """

    ERROR_CODE = None
    ERROR_MESSAGE = None

    def __call__(self, request, response, exception):
        content = self.ERROR_MESSAGE

        if request.app.debug:
            typ, value, tb = sys.exc_info()
            content = 'Status Code: %d<br/>' % self.ERROR_CODE
            content += '<br/>'.join(traceback.format_exception_only(typ, value))
            content += '<br/>'
            content += '<br/>'.join(traceback.format_tb(tb))

        response.write(content)
        response.set_status(self.ERROR_CODE)
        return response

class Handle404(ExceptionHandler):
    """ Handles 404 errors. """
    ERROR_CODE = 404
    ERROR_MESSAGE = 'The requested page was not found.'

class Handle500(ExceptionHandler):
    """ Handles 500 errors. """
    ERROR_CODE = 500
    ERROR_MESSAGE = 'An unexpected server error occurred.'