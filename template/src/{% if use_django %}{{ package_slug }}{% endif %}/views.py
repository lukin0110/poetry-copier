"""Views."""

from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    """Index view."""
    return HttpResponse("Hello Django world")
