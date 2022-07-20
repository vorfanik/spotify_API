from django.apps import AppConfig


class ApiProjectConfig(AppConfig):
    name = 'api_project'

    def ready(self):
        from .signals import create_profile, save_profile