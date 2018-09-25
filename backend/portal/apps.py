from django.apps import AppConfig


class PortalConfig(AppConfig):
    name = 'portal'

    def ready(self):
        from portal import signals