""" Models

Models should:
 - contain the db.Model definitions for accessing App Engine Datastore
 - contain all lookup methods and queries
 - communicate with the google.appengine.ext.db package

Models should not:
 - contain logic, other than logic to formulate a query
"""

from google.appengine.ext.ndb import model as ndb_model


class BaseNDBModel(ndb_model.Model):
    """ Base Model Class for all models using the NDB data layer. """

    created = ndb_model.DateTimeProperty(auto_now_add=True)
    updated = ndb_model.DateTimeProperty(auto_now=True)

    @classmethod
    def build_key(cls, entity_id, parent=None):
        """ Builds a key in the default namespace. """
        if not entity_id:
            raise ValueError('An id is required for constructing the key for %s' % cls.__name__)
        return ndb_model.Key(cls.__name__, entity_id, parent=parent)

    @classmethod
    def lookup_all(cls, keys_only=False, limit=100):
        """
        Lookup all the entities of this class.

        If keys_only=True then only the keys are returned instead of the entities.
        """
        return cls.query().fetch(limit=limit, keys_only=keys_only)
