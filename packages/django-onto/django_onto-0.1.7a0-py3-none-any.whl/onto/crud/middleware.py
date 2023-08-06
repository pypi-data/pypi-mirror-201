def htmx(view):
    """Adds attributes to the request object based on the HTMX context."""
    def middleware(request):
        request.htmx = ("HX-Request" in request.headers)
        request.modal = ("HX-Modal" in request.headers)
        return view(request)
    return middleware