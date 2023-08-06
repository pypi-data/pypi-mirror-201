from django.apps import apps
from django.db import models
from django.forms import modelform_factory
from django.http.request import HttpRequest
from django.shortcuts import redirect, render

def make_admin_list_view(model: models.Model):
    def view(request: HttpRequest):
        if not request.user.is_superuser:
            raise PermissionError("Superuser access required.")

        # pagination
        # search
        # ordering
        # ... CRUD subclass.
        
        return render(request, "onto/crud/list.html", {
            "model_meta": model._meta,
            "objects": model.objects.all()
        })

    return view

def make_admin_edit_view(model: models.Model):
    def view(request: HttpRequest, pk=None):
        if not request.user.is_superuser:
            raise PermissionError("Superuser access required.")
        
        if not hasattr(view, "Form"):
            view.Form = modelform_factory(model, exclude=[])

        instance = model.objects.filter(pk=pk).first()
        form = view.Form(request.POST or None, instance=instance)

        if request.method == "POST" and form.is_valid():
            instance = form.save()
            return redirect(f'onto_crud:edit-{model._meta.app_label}-{model._meta.model_name}', instance.pk)
        
        return render(request, "onto/crud/create.html", {
            "model_meta": model._meta,
            "object": instance,
            "form": form
        })

    return view