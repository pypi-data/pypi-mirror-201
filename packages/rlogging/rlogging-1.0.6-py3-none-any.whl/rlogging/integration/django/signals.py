import logging

from django.core.signals import *
from django.db.models.signals import *

from rlogging import namespaces

logger = logging.getLogger(namespaces.DB)

SIGNALS = [
    request_started,  # sender(django.core.handlers.wsgi.WsgiHandler) , environ(dict)
    request_finished,  # sender(django.core.handlers.wsgi.WsgiHandler)
    got_request_exception,  # sender(None), request( HttpRequest)
    setting_changed,  # sender(django.core.handlers.wsgi.WsgiHandler),
    # setting(setting Name),value(setting Value),enter(Bool)
    class_prepared,  # sender(Model class)
    pre_init,  # sender(Model class), args() , kwargs()
    post_init,  # sender(Model class), instance(Model)
    pre_save,  # sender(Model class), instance(Model),raw(Bool),using(Model verbose_name),
    # update_fields(fields | None)
    post_save,  # sender(Model class), instance(Model), created(Bool),
    # raw(Bool), using(Model verbose_name), update_fields(fields | None)
    pre_delete,  # sender(Model class), instance(Model),using(Model verbose_name)
    post_delete,  # sender(Model class), instance(Model),using(Model verbose_name)
    m2m_changed,
    # sender(Model.through class),instance(Model| AnotherModel), action, reverse, model, pk_set,using(Model verbose_name)
    pre_migrate,
    # sender(AppConfig), app_config(AppConfig), verbosity, interactive(Bool),stdout,using(Model verbose_name),
    # plan(migration plan), apps(from django.apps import apps : Apps)
    post_migrate,
    # sender(AppConfig), app_config(AppConfig), verbosity, interactive(Bool),stdout,using(Model verbose_name),
    # plan(migration plan), apps(from django.apps import apps : Apps)
]


def signal_handler(sender, *args, **kwargs):
    logger.info(
        'django signal',
        extra={
            'processing': {
                'sender': sender,
                'args': args,
                'kwargs': kwargs,
            }
        },
    )


# Connect the handler to all signals
for signal in SIGNALS:
    signal.connect(signal_handler)
