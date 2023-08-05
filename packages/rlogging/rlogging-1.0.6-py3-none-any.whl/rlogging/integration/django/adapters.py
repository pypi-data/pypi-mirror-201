from rlogging import HttpLoggerAdapter
from django.http import HttpRequest, HttpResponse
from django.core.handlers.wsgi import WSGIRequest


class DjangoLoggerAdapter(HttpLoggerAdapter):
    def request(self, request: WSGIRequest, *args, **kwargs):
        kwargs.setdefault('stacklevel', 5)

        path = request.path
        view_func = request.resolver_match

        return super().request(
            request.build_absolute_uri(),
            request.method,
            path,
            view_func,
            *args,
            **kwargs,
        )

    def response(self, response: HttpResponse, *args, **kwargs):
        kwargs.setdefault('stacklevel', 5)
        return super().response(response.status_code, *args, **kwargs)
