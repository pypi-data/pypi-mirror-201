import logging

from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from typing import Any
from rlogging.integration.django.adapters import DjangoLoggerAdapter
from rlogging import namespaces
from django.db import connection

from rlogging.utils import LazyStrCallable


class LoggingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        request.logger = DjangoLoggerAdapter(
            logging.getLogger(namespaces.HTTP), {'queries': LazyStrCallable(len, connection.queries)}
        )
        request.logger.request(request)

        response: HttpResponse = self.get_response(request)

        request.logger.queries(connection.queries)
        request.logger.response(response)

        return response

    def process_view(self, request: WSGIRequest, view_func: Any, view_args: tuple, view_kwargs: dict):
        request.logger: DjangoLoggerAdapter = request.logger
        request.logger.processing(
            request.path,
            request.resolver_match.route,
            request.resolver_match.url_name,
            view_func.__name__,
            view_args,
            view_kwargs,
            request.resolver_match.namespace,
        )

    def process_exception(self, request, exception):
        request.logger.info(
            'http process_exception',
            extra={'processing': {'exception': exception}},
        )
