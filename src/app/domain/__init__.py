""" Domain

The domain-layer should:
 - contain all business logic
 - be well unit-tested

The domain-layer should not:
 - access google.appengine.ext.db directly - call the model layer for that
"""

def entity_to_obj(cls, entity):
    """ Translates an entity to a domain object. """
    if not entity:
        return None

    # pylint: disable=W0212
    # access to protected member _properties. It seems this is the only way to do it
    kwargs = {}
    for prop in entity._properties:
        if not prop.startswith("_") and hasattr(entity, prop):
            kwargs[prop] = getattr(entity, prop)

    instance = cls(**kwargs)
    return instance
