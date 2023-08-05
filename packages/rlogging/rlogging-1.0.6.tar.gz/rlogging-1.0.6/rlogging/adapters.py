import logging
import uuid

from typing import Any


class RsLoggerAdapter(logging.LoggerAdapter):
    """Путь логирования

    Создание логов, через флоу позволяет обоготить их

    """

    flow_id: uuid.UUID

    def __init__(self, logger: logging.Logger, extra: dict | None = None) -> None:
        extra = extra if extra is not None else {}

        super().__init__(logger, extra)

        self.flow_id = uuid.uuid1()

    def _extra_update(self, kwargs: dict, extra: dict):
        kwargs['extra'] = extra | kwargs.get('extra', {})

    def process(self, msg: Any, kwargs: dict) -> tuple[Any, dict]:
        kwargs.setdefault('stacklevel', 2)

        extra = {
            'flow_id': self.flow_id,
        }

        self._extra_update(kwargs, extra)
        self._extra_update(kwargs, self.extra)

        return msg, kwargs


class AppLoggerAdapter(RsLoggerAdapter):
    def queries(self, queries: list, *args, **kwargs):
        kwargs.setdefault('stacklevel', 4)
        self.info(f'processing queries: {len(queries)}', *args, **kwargs)


class HttpLoggerAdapter(AppLoggerAdapter):
    """Флоу для логирования веб запросов/ответов"""

    def request(
        self,
        url: str,
        method: str,
        *args,
        **kwargs,
    ):
        kwargs.setdefault('stacklevel', 3)

        extra = {
            'http': {
                'url': url,
                'method': method,
            }
        }
        self._extra_update(kwargs, extra)

        self.info('http request', *args, **kwargs)

    def response(self, code: int, *args, **kwargs):
        kwargs.setdefault('stacklevel', 3)

        extra = {
            'http': {
                'code': code,
            },
        }
        self._extra_update(kwargs, extra)

        self.info('http response', *args, **kwargs)

    def processing(
        self,
        path: str,
        route: str,
        route_name: str,
        view: str,
        view_args: tuple,
        view_kwargs: dict,
        namespace: str,
        *args,
        **kwargs,
    ):
        kwargs.setdefault('stacklevel', 4)

        extra = {
            'processing': {
                'path': path,
                'route': route,
                'route_name': route_name,
                'view': view,
                'view_args': view_args,
                'view_kwargs': view_kwargs,
                'namespace': namespace,
            },
        }
        self._extra_update(kwargs, extra)

        self.info('http process_view', *args, **kwargs)
