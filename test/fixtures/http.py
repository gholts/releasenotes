""" See here for information regarding testing webapp2:
        http://webapp-improved.appspot.com/guide/testing.html
"""
from webapp2 import Request
from webob.multidict import MultiDict

def create_request(path='/', **kwargs):
    """ Creates a Request object. """
    return Request.blank(path=path, **kwargs)

def create_form(form_class, **kwargs):
    """ Creates a form and populates it with the kwargs. """
    return form_class(MultiDict(kwargs))