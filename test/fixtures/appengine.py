""" Contains Test Fixtures for Google AppEngine dependencies """

import unittest
from minimock import Mock, restore as minimock_restore
from google.appengine.ext import testbed
from google.appengine.api import urlfetch
from google.appengine.api.namespace_manager import get_namespace, set_namespace

class GaeTestCase(unittest.TestCase):
    """ Defines TestCase for testing App Engine code. See here for more info:
            http://code.google.com/appengine/docs/python/tools/localunittesting.html
    """

    def setUp(self):
        self._old_namespace = get_namespace()
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub()

    def tearDown(self):
        """ Tears down the test environment. """
        self.testbed.deactivate()
        minimock_restore()
        set_namespace(self._old_namespace)
        super(GaeTestCase, self).tearDown()

    def mock_urlfetch(self):
        """ Mock appengine's urlfetch.
            self.response can then be modified to whatever urlfetch should return.
            self.response.raises will be raised to whichever exception it is set to.

            Instructions:
                Call self.mock_urlfetch() in setUp()
                Then self.response to whatever you want returned from the urlfetch for that test:
                    Eg. self.response.content = 'this is a urlfetch response'
                        self.response.raises = urlfetch.DownloadError

        """
        # disables urlfetch to ensure we don't inadvertently go over the wire
        self.testbed.init_urlfetch_stub(enable=False)

        self.response = UrlFetchResponseMock()

        # pylint: disable=E0702
        # Raising NoneType while only classes, instances or string are allowed
        # pylint: disable=W0613
        # Unused argument 'args' and 'kwargs'
        def fetch_mock(*args, **kwargs):
            if self.response.raises:
                raise self.response.raises
            return self.response
        
        # pylint: disable=W0612
        # Unused variable 'google'
        import google.appengine.api.urlfetch
        urlfetch.fetch = Mock('urlfetch.fetch', returns_func=fetch_mock, tracker=None)

class UrlFetchResponseMock(object):

    def __init__(self):
        self.raises = None
        self.content = ''
        self.content_was_truncated = False
        self.status_code = 200
        
        from datetime import datetime
        header_date = datetime.now().strftime('%a, %d %b %Y %H:%m:%S')
        self.headers = {
            'content-length': '100',
            'vary': 'Accept-Encoding',
            'server': 'Google Frontend',
            'cache-control': 'private',
            'date': header_date,
            'content-type': 'application/json'
        }