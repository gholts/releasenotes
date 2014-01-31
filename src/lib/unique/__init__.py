""" Utility to build unique constraint. """

# lib imports
from google.appengine.ext.ndb import model

# webapp2 imports
from webapp2_extras.appengine.auth.models import Unique


def build_unique_value(constraint_name, *values):
    """ Builds a key_name using the constaint_name and arbitrary args. """
    if not constraint_name:
        raise ValueError('constraint_name is required.')
    if len(values) == 0:
        raise ValueError('You must provide at least one value.')
    value_str = ':'.join(values)
    constraint = '%s:%s' % (constraint_name, value_str)
    if len(constraint) >= 500:
        raise ValueError("Unique constraint would exceed 500 char limit for DS keys")
    return constraint

def set_unique(constraint_name, *values):
    """ Sets up a unique constraint.

    @param constraint_name the name of the constraint, used to partition the values
    @param *values a list of values that are part of the unique constraint
    @param **kwargs namespace the namespace to use instead of the namespace manager
    @raises UniqueConstraintViolatedException if the unique constraint is violated
    """
    value = build_unique_value(constraint_name, *values)
    status = Unique.create(value)
    if not status:
        raise UniqueConstraintViolatedException(
                'Constraint "%s" for values "%s" already exists.' % (constraint_name, ', '.join(values))
                                )

def clear_unique(constraint_name, *values):
    """ Clears a unique constraint.

    @param constraint_name the name of the constraint, used to partition the values
    @param *values a list of values that are part of the unique constraint
    @param **kwargs namespace the namespace to use instead of the namespace manager
    """
    value = build_unique_value(constraint_name, *values)
    Unique.delete_multi([value])

def is_unique_key(constraint_name, *values):
    """ check if key is unique
        True if unique key
        False if key is not available
    @param constraint_name the name of the constraint, used to partition the values
    @param *values a list of values that are part of the unique constraint
    @param **kwargs namespace the namespace to use instead of the namespace manager
    """
    value = build_unique_value(constraint_name, *values)
    key = model.Key(Unique, value)
    return not key.get()

class UniqueConstraintViolatedException(Exception):
    """
        Raised if a unique constraint is violated.
        message = the description of the exception
    """
    def __init__(self, message):
        self.message = message
        super(UniqueConstraintViolatedException, self).__init__(None, message)

