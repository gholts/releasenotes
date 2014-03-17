"""
API endpoints
"""
import datetime
import logging
import json
import os
import time
import webapp2

from google.appengine.ext import ndb

__all__ = ['ApiHandler', 'ValidationError', 'GET_METHOD', 'POST_METHOD', 'JSON_CONTENT_TYPE']

IS_DEV_SERVER = 'development' in os.environ.get('SERVER_SOFTWARE', '').lower()
POST_METHOD = "post"
GET_METHOD = "get"
JSON_BODY = "json"
VALID_POST_BODIES = frozenset([JSON_BODY])
JSON_CONTENT_TYPE = 'application/json'
VALID_METHODS = frozenset([GET_METHOD, POST_METHOD])

class ApiHandler(webapp2.RequestHandler):
    """
    ApiHandler for all APIs for this app
    """
    API_USER_KEY = "apiUser"
    API_KEY_KEY = "apiKey"
    STATUS_CODE_KEY = 'statusCode'
    MESSAGE_KEY = 'message'
    VERSION_KEY = 'version'
    RESPONSE_TIME_KEY = 'responseTime'
    REQUEST_ID_KEY = 'requestId'
    DATA_KEY = 'data'
    PAGE_SIZE_KEY = 'pageSize'
    NEXT_URL_KEY = 'nextUrl'
    NEXT_QUERY_STRING = 'nextQueryString'
    TOTAL_RESULTS_KEY = 'totalResults'
    CURSOR_KEY = 'cursor'
    QUERY_KEY = 'query'
    NUMBER_FOUND_ACCURACY_KEY = 'numberFoundAccuracy'
    LOG_KEY = 'log'
    DEPRECATED_WARNINGS_KEY = 'deprecationWarnings'

    ALLOWED_METHODS = frozenset([GET_METHOD, POST_METHOD])
    ALTERNATE_POST_BODY = ''
    DEFAULT_VALUES = {}
    DOC_DEPRECATED = ''
    DOC_DEPRECATED_ARGS = {}
    ISO_DATE_FORMAT_STR = '%Y-%m-%d'
    ISO_TIME_FORMAT_STR = '%H:%M:%SZ'
    ISO_DATETIME_FORMAT_STR = '%Y-%m-%dT%H:%M:%SZ'
    REQUIRED_ARGS = frozenset([])
    REQUIRES_HTTPS = True
    ALWAYS_ALLOWED_ARGS = frozenset(['apiUser', 'apiKey', 'pageSize', 'cursor', 'query', 'log', 'numberFoundAccuracy'])
    VERSION = "0.0"

    # R0912:239,4:ApiHandler.__init__: Too many branches (22/20)
    # R0915:411,4:ApiHandler.__init__: Too many statements (83/70)
    # lots to validate!
    def __init__(self, *args, **kwargs): # pylint: disable=R0912,R0915
        """
        Init
        """
        super(ApiHandler, self).__init__(*args, **kwargs)
        self.message       = None
        self._stime        = time.time()
        self._api_user     = None
        self._api_key      = None
        self.response_time = None
        if not self.VERSION:
            raise ValueError('VERSION must be specified.')
        if not isinstance(self.VERSION, str):
            raise ValueError('VERSION must be a string.')
        try:
            major, minor = self.VERSION.split('.')
            int(major)
            int(minor)
        except Exception:
            raise ValueError('VERSION must be "x.y" where x and y are integers.')
        if not self.ALLOWED_METHODS:
            raise ValueError('ALLOWED_METHODS must be specified.')
        if not isinstance(self.ALLOWED_METHODS, (list, tuple, frozenset, set)):
            raise ValueError('ALLOWED_METHODS must be iterable.')
        for method in self.ALLOWED_METHODS:
            if method not in VALID_METHODS:
                raise ValueError('ALLOWED_METHOD "%s" is not in valid set "%s".' % (method, VALID_METHODS))
        if self.ALTERNATE_POST_BODY and self.ALTERNATE_POST_BODY not in VALID_POST_BODIES:
            raise ValueError('ALTERNATE_POST_BODY "%s" is not in valid set "%s".' % \
                             (self.ALTERNATE_POST_BODY, VALID_POST_BODIES))
        self._alternate_post_body = None
        if not isinstance(self.DEFAULT_VALUES, dict):
            raise ValueError('DEFAULT_VALUES must be a dict.')
        if not isinstance(self.REQUIRED_ARGS, (list, tuple, frozenset, set)):
            raise ValueError('REQUIRED_ARGS must be iterable')
        if hasattr(self, 'ALLOWED_ARGS'):
            if not isinstance(self.ALLOWED_ARGS, (list, tuple, frozenset, set)):
                raise ValueError('ALLOWED_ARGS must be iterable')
        group = getattr(self, 'RATE_LIMIT_GROUP', None)
        if group and not isinstance(group, str):
            raise ValueError('Rate limit group "%s" must be a string.' % group)
        if not isinstance(self.DOC_DEPRECATED, basestring):
            raise ValueError('DOC_DEPRECATED must be a basestring.')
        if not isinstance(self.DOC_DEPRECATED_ARGS, dict):
            raise ValueError('DOC_DEPRECATED_ARGS must be a str.')

    def initialize(self, *args, **kwargs):
        """
        Initialize the handler. Invoked on each request.
        """
        super(ApiHandler, self).initialize(*args, **kwargs)
        self.message = None
        self._stime = time.time()
        self._api_user = None
        self._api_key = None

    @ndb.toplevel
    def dispatch(self):
        """
        The main request handler entry point.
        """
        content_disposition = None

        args = {}
        try:
            self.validate_scheme()
            self.validate_credentials()
            self.validate_method()
            request_args = self.get_request_args()
            args = self.get_cleaned_args(request_args)
            serialized_result = self.generate_serialized_response(args)
            content_type = self.get_content_type(args)
            content_disposition = self.get_content_disposition(args)
        except Exception, e:
            self.response.status_int = getattr(e, 'status_int', 500)
            serialized_result = self.generate_serialized_exception_response(args, e)
            content_type = self.get_content_type_exception_response(args)
        if content_type:
            self.response.headers.add('Content-type', content_type)
        if content_disposition:
            self.response.headers.add('Content-Disposition', content_disposition)
        self.response.out.write(serialized_result)

    # R0912:604,4:ApiHandler.get_cleaned_args: Too many branches (21/20)
    def get_cleaned_args(self, request_args):  # pylint: disable=R0912
        """
        Returns a cleaned dict of all args. Converts ISO dates to datetime. Strips strings.
        Multiple arguments will become lists; note: even if a particular argument supports a multiple interface,
        a single input will appear as a single, non-list value.
        """
        args = {}
        for key, default in self.DEFAULT_VALUES.iteritems():
            args[key] = default

        for key in request_args:
            result = []
            all_values = self.get_all_values(key) if isinstance(request_args, list) else request_args[key]
            for value in all_values:
                if isinstance(value, basestring):
                    result.append(value.strip())
                # TODO: any way to handle ints/floats? Likely not. Leave it up the subclass.
                else:
                    result.append(value)
            if len(result) == 0:
                args[key] = None
            elif len(result) == 1:
                if result[0] == '':
                    args[key] = None
                else:
                    args[key] = result[0]
            else:
                args[key] = result
        return args

    # W0613:609,34:ApiHandler.get_content_type: Unused argument 'args'
    # virtual interface for the subclass
    def get_content_type(self, args): # pylint: disable=W0613
        """
        Returns the content-type for the response. Override to return a dynamic content type.
        """
        return JSON_CONTENT_TYPE

    # W0613:609,34:ApiHandler.get_content_type_exception_response: Unused argument 'args'
    # virtual interface for the subclass
    def get_content_type_exception_response(self, args): # pylint: disable=W0613
        """
        Returns the content-type for the exception response. Override to return a dynamic content type.
        To change browser filename download behavior, use with get_content_disposition
        """
        return JSON_CONTENT_TYPE

    def generate_serialized_exception_response(self, args, e):
        """
        In case of an exception, this method generates the serialized response for the exception.
        Typically, this would be overridden with generate_serialized_response.
        """
        try:
            if isinstance(e, webapp2.exc.HTTPServerError):
                logging.error('A server API error occurred.', exc_info=True)
            elif isinstance(e, webapp2.exc.HTTPClientError):
                logging.warn('A client API error occurred.', exc_info=True)
            else:
                logging.error('An unexpected error occurred.', exc_info=True)
            if self.message:
                logging.info('Message "%s" was overwritten.', self.message)
            self.message = getattr(e, 'detail', e.message)
            logging.info('Message sent to client was "%s".', self.message)
            result = self.generate_meta_result(args)
            serialized_result = json.dumps(result)
        except Exception:
            logging.critical('Exception handling completely failed. Sending basic 500 to client.',
                             exc_info=True)
            self.response.status_int = 500
            serialized_result = '{"%s":500}' % self.STATUS_CODE_KEY
        return serialized_result

    def generate_meta_result(self, args):
        """
        Returns the top-level dictionary filled with the meta information.
        """
        result = {
            self.STATUS_CODE_KEY   : self.response.status_int,
            self.VERSION_KEY       : self.VERSION,
            self.RESPONSE_TIME_KEY : self.generate_response_time(),
        }
        if self.message:
            result[self.MESSAGE_KEY] = self.message
        result = self.add_deprecation_warnings(result, args)
        result = self.augment_meta_result(result, args)
        return result

    # W0613:311,47:ApiHandler.augment_meta_result: Unused argument 'args'
    # just an abstract method
    def augment_meta_result(self, meta_result, args): # pylint: disable=W0613
        """
        Allows a subclass to add information to the meta dictionary.
        """
        return meta_result

    def get_content_disposition(self, args): # pylint: disable=W0613
        """
        Returns the content-disposition, should be used with get_content_type
        """
        return None

    def generate_serialized_response(self, args):
        """
        Generates a serialized response. Override this method to generate an alternate response body.
        """
        data = None
        try:
            args = self.pre_process_hook(args)
            data = self.process(args) # let the child class actually do its work!
            data = self.post_process_hook(args, data)
        except ValidationError as e:
            self.abort(400, detail=e.message)
        except Exception as e:
            data = self.handle_process_exception(e, args)
        data = self.serialize_datatypes(data)
        result = self.generate_meta_result(args)
        result[self.DATA_KEY] = data
        serialized_result = json.dumps(result)
        return serialized_result

    def get_all_values(self, key):
        """
        Returns the post values for the specified key
        """
        all_values = self.request.get_all(key)
        if JSON_BODY == self.ALTERNATE_POST_BODY:
            for k, v in self.get_json_body.iteritems():
                if key == k:
                    all_values.append(v)
            return all_values

        return all_values

    @webapp2.cached_property
    def get_json_body(self):
        """
        Decode the json string from the request body
        """
        if not self._alternate_post_body:
            try:
                self._alternate_post_body = json.loads(self.request.body)
            except ValueError:
                self._alternate_post_body = {}
                logging.info('Failed to deserialize POST body as JSON, continuing under the assumption that ' +
                             'the client is using standard form encoding. Posted body: %s', self.request.body)
        return self._alternate_post_body

    def generate_response_time(self):
        """
        Generates the response time, but only once per request.
        """
        if self.response_time is  None:
            etime = time.time()
            self.response_time = int((etime - self._stime) * 1000)
        return self.response_time

    def get_request_args(self):
        """
        Returns the current requests arguments.
        """
        request_args = self.request.arguments()
        if JSON_BODY == self.ALTERNATE_POST_BODY:
            request_args.extend(self.get_json_body.iterkeys())

        return request_args

    # W0613:265,39:ApiHandler.handle_process_exception: Unused argument 'e'
    # virtual interface for the subclass
    def handle_process_exception(self, e, args): # pylint: disable=W0613
        """
        Allow subclass the opportunity to handle a process exception in a custom way.
        Can raise a different exception, or return an alternate data dictionary (i.e., like
        the process return type).
        """
        raise

    def process(self, args):
        """
        Override to actually do the work. Should return the "data" dictionary (or list).
        """
        raise NotImplementedError()

    def pre_process_hook(self, args):
        """
        Called immediately before the process() call, typically so that the args dictionary can be
        adjusted. If a ValidationError is raised in this method, a 400 response will be generated.
        This method should return an args dictionary, which is passed directly to process().
        """
        return args

    # W0613:663,32:ApiHandler.post_process_hook: Unused argument 'args'
    # virtual interface for the subclass
    def post_process_hook(self, args, data): # pylint: disable=W0613
        """
        Called immediately after the process() call. args is the dictionary of args that had been
        passed to process() and data is the data that was returned from process. If a ValidationError
        is raised in this method, a 400 response will be generated. This method should return
        the data that will be serialized (i.e., similar to the process() output).
        """
        return data

    @classmethod
    def serialize_datatypes(cls, data):
        """
        Walk through the data and serialize datetime, date, time.
        """
        if isinstance(data, list):
            return [cls.serialize_datatypes(item) for item in data]
        if isinstance(data, dict):
            return dict([(k, cls.serialize_datatypes(v)) for k, v in data.iteritems()])
        if isinstance(data, datetime.datetime):
            return data.strftime(cls.ISO_DATETIME_FORMAT_STR)
        if isinstance(data, datetime.date):
            return data.strftime(cls.ISO_DATE_FORMAT_STR)
        if isinstance(data, datetime.time):
            return data.strftime(cls.ISO_TIME_FORMAT_STR)
        return data

    def validate_credentials(self):
        """
        Ensure that the caller's credentials are in order.
        """
        self._api_user = self.request.GET.get(self.API_USER_KEY)
        self._api_key  = self.request.GET.get(self.API_KEY_KEY)
        if not self._api_user or not self._api_key:
            self.abort(400, detail='%s and %s are required for this end-point.' % \
                            (self.API_USER_KEY, self.API_KEY_KEY))
        if not self.check_credentials(self._api_user, self._api_key):
            self.abort(401, detail='Invalid %s/%s combination.' % (self.API_USER_KEY, self.API_KEY_KEY))

    def validate_method(self):
        """
        Ensures that the correct HTTP method is being used. This validation does nothing on dev appserver.
        """
        if IS_DEV_SERVER:
            return
        if self.request.method.upper() == POST_METHOD:
            return # POST is always supported due to GET url limitations in App Engine
        if self.request.method.upper() not in self.ALLOWED_METHODS:
            self.abort(405, detail='Method "%s" not in allowed methods "%s".' % \
                                   (self.request.method, self.ALLOWED_METHODS))

    def validate_scheme(self):
        """
        Validates that the scheme is HTTPS.
        """
        if IS_DEV_SERVER:
            return # don't require HTTPS on dev_appserver
        if not self.REQUIRES_HTTPS:
            return
        if self.request.scheme.lower() != 'https':
            self.abort(403, detail='HTTPS is required for this end-point.')

    def check_credentials(self, api_user, api_key): # pylint: disable=W0613
        """
        Checks that the credentials are correct. An unknown apiUser should return False. An invalid apiUser/apiKey
        combination should return False.
        """
        raise NotImplementedError()

    def add_deprecation_warnings(self, meta_result, args):
        """
        Adds deprecation warnings to the meta dictionary.
        """
        if not self.DOC_DEPRECATED and not self.DOC_DEPRECATED_ARGS:
            return meta_result
        try:
            deprecated = {}
            if self.DOC_DEPRECATED:
                deprecated['__api__'] = self.DOC_DEPRECATED
            for arg in args.iterkeys():
                if arg in self.DOC_DEPRECATED_ARGS.keys():
                    deprecated[arg] = self.DOC_DEPRECATED_ARGS[arg]
            if deprecated:
                meta_result[self.DEPRECATED_WARNINGS_KEY] = deprecated
        except Exception:
            logging.warn('Failed to add deprecation warnings. Continuing.', exc_info=True)
        return meta_result

class ValidationError(Exception):
    """
    Raised for a validation error.
    """
