""" Meta handlers for general site hosting. """

import datetime
from app.views import BaseHandler

class SitemapXmlHandler(BaseHandler):
    """ Handler for /sitemap.xml requests. """

    def get(self):
        """ GET """
        context = { 'hostname': self.request.host }
        self.response.charset = 'utf-8'
        self.response.content_type = 'text/xml'
        cache_seconds = 2 * 60 * 60
        self.response.expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=cache_seconds)
        self.response.headers['Cache-Control'] = 'public, max-age=%d' % cache_seconds
        self.render_response('xml/sitemap.xml', **context)
