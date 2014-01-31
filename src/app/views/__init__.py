""" Views

Views should:
 - choose an appropriate template
 - call only the app.domain layer
 - convert data from the domain layer to a template-consumable format
 - convert incoming parameters to a domain-consumable format
 - error check incoming values
 - provide meaningful HTTP response error codes
 - enforce authentication and authorization

Views should not:
 - call the model layer
 - perform logic, other than to convert data into an appropriate format
"""

import webapp2
import simplejson

from webapp2_extras import jinja2, sessions

FLASH_KEY = "base-webapp2-jinja2_flash_key"

class BaseHandler(webapp2.RequestHandler):
    """ The base handler for all handlers."""

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.session_store = None


    def dispatch(self):
        """ Get a session store for this request. """
        # pylint: disable=W0201
        # self.session_store defined outside init. this is defined in webapp2.RequestHandler
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def jinja2(self):
        """ Returns a Jinja2 renderer cached in the app registry. """
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, template, **context):
        """ Renders a template and writes the result to the response. """
        context['flashes'] = self.get_flashes()
        rv = self.jinja2.render_template(template, **context)
        self.response.write(rv)

    @property
    def session(self):
        """ Returns a session using the datastore key. """
        return self.session_store.get_session(backend='datastore')

    def get_flashes(self, key=FLASH_KEY):
        """
        Retrieves flash with an optional key from the current session.
        [
            {
                'title': 'Error',
                'text': 'file: This field is required.',
                'sticky': True,
                ...
            },
            {
                'title': 'Success',
                'text': 'Message has been sent.',
                ...
            }
        ]
        """
        return [simplejson.loads(flash[0]) for flash in self.session.get_flashes(key=key)]

    def set_flash(self, text, title=None, key=FLASH_KEY, **kwargs):
        """ Sets flash with an optional key for the current session. """
        flash = {
            'text' : text
        }
        flash.update(kwargs.items())
        if title:
            flash['title'] = title
        self.session.add_flash(simplejson.dumps(flash), key=key)


class BaseJsonHandler(webapp2.RequestHandler):
    """ The base handler for json handlers ."""

    def __init__(self, *args, **kwargs):
        super(BaseJsonHandler, self).__init__(*args, **kwargs)


    def render_response(self, data):
        """ Renders a json response """

        self.response.content_type = 'text/json'
        self.response.write(data)

