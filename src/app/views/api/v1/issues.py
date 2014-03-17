"""
API Endpoints for Issues
"""
import json

from app.views.api import ApiHandler
from keys import API_KEY
from app.domain.format import format_email_text

class FormatMixin(ApiHandler):
    """
    Helper stuff for Format API
    """
    def check_credentials(self, api_user, api_key):
        if api_user in API_KEY.API_USERS:
            if api_key == API_KEY.API_KEYS[api_user]:
                return True
        return False

class FormatApi(FormatMixin):
    """
    Handles requests to the format API
    """
    REQUIRES_HTTPS = False
    REQUIRED_ARGS = frozenset([API_KEY.ISSUE_LIST, API_KEY.PRODUCTS])
    ALLOWED_ARGS = frozenset([API_KEY.FORMAT_TYPE])
    VERSION = "1.0"
    URL = "/api/v1/issues/format/"

    def process(self, args):
        issue_list = json.loads(args[API_KEY.ISSUE_LIST])
        products = args[API_KEY.PRODUCTS]
        format_type = args.get(API_KEY.FORMAT_TYPE)
        formatted_issues = format_email_text(issue_list, products, issue_format=format_type)

        return formatted_issues