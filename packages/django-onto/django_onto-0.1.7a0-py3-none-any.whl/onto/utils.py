import re

from django.utils.text import slugify


def get_entity_pk(obj):
    """
    Return the PK of the 'primary' Entity associated with this object, based on its `entity_pk_field` attribute.
    """
    try:
        return getattr(obj, obj.entity_pk_field)
    except AttributeError as e:
        raise AttributeError(f"{repr(obj)} cannot be resolved to an Entity because it is missing an 'entity_pk_field' attribute.") from e