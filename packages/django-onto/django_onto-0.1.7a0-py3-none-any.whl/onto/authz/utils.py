from onto.models import Entity, EntityModel

def obj_to_entity(obj):
    if isinstance(obj, EntityModel):
        return obj.entity
    elif isinstance(obj, Entity):
        return obj
    #elif hasattr(obj, "authz_proxy"):
    #    return obj_to_entity(getattr(obj, obj.authz_proxy))
    else:
        return None

# Snippet from GvR: https://mail.python.org/pipermail/python-dev/2008-January/076194.html
def monkeypatch_method(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator