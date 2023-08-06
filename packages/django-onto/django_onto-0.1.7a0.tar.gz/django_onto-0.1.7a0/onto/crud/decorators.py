from collections import defaultdict, namedtuple

from django.db import models
from django.urls import path

from .views import make_admin_edit_view, make_admin_list_view

URLs = namedtuple("URLs", ("pattern_list", "app_namespace"))

def admin_crud(model: models.Model):
    """
    Generates a CRUD GUI for this Model, accessible only to superusers.
    """

    app_label = model._meta.app_label
    model_name = model._meta.model_name

    if model in admin_crud.registry[app_label]:
        raise ValueError(f"{model} has already been registered as a CRUD model.")

    admin_crud.registry[app_label].add(model)

    list_view = make_admin_list_view(model)
    edit_view = make_admin_edit_view(model)
    admin_crud.urls.pattern_list.append(path(f"{app_label}/{model_name}/", list_view, name=f"list-{app_label}-{model_name}"))
    admin_crud.urls.pattern_list.append(path(f"{app_label}/{model_name}/edit", edit_view, name=f"create-{app_label}-{model_name}"))
    admin_crud.urls.pattern_list.append(path(f"{app_label}/{model_name}/edit/<pk>", edit_view, name=f"edit-{app_label}-{model_name}"))

    return model

admin_crud.registry = defaultdict(set)
admin_crud.urls = URLs(
    app_namespace="onto_crud",
    pattern_list=list(), 
)