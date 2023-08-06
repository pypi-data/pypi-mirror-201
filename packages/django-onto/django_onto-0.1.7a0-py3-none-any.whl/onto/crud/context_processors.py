def base_template(request):
    template = "dash/base.html"
    if request.htmx:
        if request.modal:
            template = "dash/base_modal.html"
        else:
            template = "dash/base_ajax.html"

    print(f"base_template: {template}")
    return {"base_template": template}