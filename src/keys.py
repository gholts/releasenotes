""" Module containing dict keys for the app """
import os
import re

class KEY(object):
    """
    All dictionary keys used by the app
    """

    URL_ROOT                    = '/'
    URL_NAME_ROOT               = 'home'
    URL_SITEMAP_XML             = '/sitemap.xml'
    URL_NAME_SITEMAP_XML        = 'sitemap-xml'

    IS_LOCAL_DEV                = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

    # note: regex retreived from http://www.regular-expressions.info/email.html
    # it is a regex implementation of RFC 2822
    # pylint: disable-msg=C0301
    # C0301: 21: Line too long (436/120)
    # This is a crazy regex string literal that needs to be long.
    EMAIL_REGEX_EXPRESSION = re.compile(
        """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    )
    # at least one character and one number, at least 6 characters
    PASSWORD_REGEX_EXPRESSION = re.compile("^.*(?=.{6,})(?=.*\d)(?=.*[a-zA-Z]).*$")