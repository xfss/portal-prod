from django.apps import AppConfig


class StatusConfig(AppConfig):
    name = 'status'

    def ready(self):
        from status import signals
