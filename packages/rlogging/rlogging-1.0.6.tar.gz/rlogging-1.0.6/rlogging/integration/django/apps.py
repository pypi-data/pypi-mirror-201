from django.apps import AppConfig


class RLoggingDjangoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rlogging.integration.django'
    label = 'rlogging_integration_django'

    def ready(self):
        from . import signals
