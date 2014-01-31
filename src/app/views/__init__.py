import logging

from google.appengine.api import users
from webapp2 import RequestHandler, cached_property
from webapp2_extras import jinja2

import json


class TemplatedView(RequestHandler):

    @cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, template, **context):
        """ Pass a template (html) and a dictionary :) """
        content = self.jinja2.render_template(template, **context)
        self.response.write(content)

